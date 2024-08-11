# Wei-ban Course Helper NWPU ver. 1.0
# Do not use it for illegal purposes.
# Do not distribute!

import asyncio
import functools
import sys
import time
from datetime import datetime

import config
import json_structs
import ui_helper
import web_utils
from config import *


def dbg_print(msg: str):
    if DEBUG:
        now: datetime = datetime.now()
        print(f"[DEBUG] [{now}] {msg}")


async def main():
    session = None

    if input("Use normal login method or use cookie? \nInput 1 for cookie, otherwise normal login. >>").strip() == "1":
        token = input("Token here >>").strip()
        user_id = input("User ID here >>").strip()
        tenant_code = input("Tenant code here (press enter to use school name instead) >>").strip()
        if tenant_code == "":
            school_name = input("School name here >>").strip()
            tenant_code = web_utils.fetch_all_tenants()[school_name]
        session = json_structs.User(
            token=token,
            user_id=user_id,
            tenant=tenant_code
        )

    else:
        tenants = web_utils.fetch_all_tenants()
        dbg_print(str(len(tenants)))

        while (inp := input("Your school name here >>").strip()) not in tenants.keys():
            print("School not found:", inp, ". Please try again.")

        my_tenant = tenants[inp]
        dbg_print(my_tenant)

        uname_prompt, pwd_prompt = web_utils.fetch_tenant_conf(my_tenant)
        print("Customized username prompt:", uname_prompt)
        user_name = input("Username here >>").strip()

        print("Customized pwd prompt:", pwd_prompt)
        pwd = input("Password here >>").strip()

        while session is None:
            captcha, ts_sec = web_utils.fetch_login_captcha()
            print("After viewing the CAPTCHA, close the window to continue.")
            ui_helper.display_img(captcha.content)
            captcha_result = input("CAPTCHA here >>")

            session, msg = await web_utils.login(my_tenant, user_name, pwd, captcha_result, ts_sec)
            if session is None:
                print("Error occurred. Please retry.", msg)

    if session is None:
        print("FATAL: login failed with bad return value.")
        sys.exit(0)

    # IMPORTANT!!!
    web_utils.set_token(session.token)

    print("Start fetching all ongoing projects...")
    projects: list[json_structs.Project] = await web_utils.fetch_project_list(session.tenant_code, session.user_id)

    for p in projects:
        start = time.time()

        courses: list[json_structs.Course] = list()
        print("Ongoing project:", p.project_name, "ID:", p.project_id, "User Project ID:", p.user_project_id)
        categories: list[json_structs.Category] = \
            await web_utils.fetch_category_list(session.tenant_code, session.user_id, p.user_project_id)

        task_courses: list = list()
        for c in categories:
            print("Ongoing category:", c.category_name, "ID:", c.category_code)
            if (not c.finished) or (not IGNORE_FINISHED_TASKS):
                task_courses.append(
                    asyncio.create_task(
                        web_utils.fetch_course_list(session.tenant_code, session.user_id,
                                                    p.user_project_id, c.category_code)
                    )
                )
        print("Starting to fetch ongoing courses asynchronously...")
        courses = functools.reduce(lambda x, y: x + y, await asyncio.gather(*task_courses))
        print("Detected", len(courses), "courses to be finished.")
        tasks: list = list()

        cnt = 0
        for c in courses:
            tasks.append(
                asyncio.create_task(
                    web_utils.learn_course(session.tenant_code, session.user_id,
                                           p.user_project_id, c.user_course_id, c.resource_id,
                                           c.resource_name, session.user_name)
                )
            )

            cnt += 1
            if cnt >= MAX_TASK_NUM:
                break

        print("Gathered", total_cnt := len(tasks), "tasks in total. Starting coroutines...")
        result = await asyncio.gather(*tasks)

        end = time.time()

        success_cnt = 0
        for r in result:
            if r:
                success_cnt += 1

        time_elapsed = end - start
        print("Succeeded tasks:", success_cnt, "of", total_cnt, end=".\n")
        print("Ongoing task of Project", p.project_name, "successfully terminated in", time_elapsed, "secs.")

    print("All ongoing tasks successfully terminated.")


if __name__ == "__main__":
    config.parse_conf()
    asyncio.run(main())
