import sys

from . import fake_env, fake_user, fake_user_session, fake_account_recovery_request

sys.modules['blueprints.utils.env_variables'] = fake_env
sys.modules['FCClass.user'] = fake_user
sys.modules['FCClass.user_session'] = fake_user_session
sys.modules['FCClass.account_recovery_request'] = fake_account_recovery_request
