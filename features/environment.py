from behave import *

from features.fixtures import *


def before_all(context):
    use_fixture(browser_chrome, context)
    use_fixture(timeout_for_page_load, context)


def after_step(context, step):
    # FUNCTION TO ACTIVATE IPDB DEBUGGER EVERYTIME AN ERROR OCCURS:
    if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        import ipdb
        ipdb.post_mortem(step.exc_traceback)


def before_step(context, step):
    # FIXTURE THAT ENSURES THAT PRELOADER HAS ALREADY FINISH LOADING THE PAGE ON E-COMMERCE PAGES
    use_fixture(invisibility_of_preloader, context)

