from logan_user.User_side_all_feature import User_Side_All_Feature
from logan_admin.admin_auth import Auth
import pytest



class Test_runner:


    action = User_Side_All_Feature()
    # def test_login_admin(self):
    #     auth = Auth()
    #     auth.login_admin()

    @pytest.fixture(scope="function")
    def userdata(self):
        responce = self.action.login_user()
        token = responce["token"]
        user = responce["userdata"]
        print(user)
        return {"token": token,"user": user}


    def test_login_user(self):
        self.token = self.action.login_user()["token"]
        self.userdata = self.action.login_user()["userdata"]

    def test_user_details(self,userdata):
        self.action.login_user_details(userdata["token"],userdata["user"])

    def test_user_deposit_amount_to_wallet(self,userdata):
        self.action.deposit_amount(userdata["token"],100,userdata["user"])

    def test_user_deposit_transaction(self,userdata):
        self.action.transaction_deposit(userdata["token"],100,userdata["user"])

    def test_user_withdrawal_amount_to_wallet(self,userdata):
        self.action.withdrawal_amount(userdata["token"],10,userdata["user"])

    def test_user_withdrawal_transaction(self,userdata):
        self.action.transactions_withdraw(userdata["token"],10,userdata["user"])

    def test_user_profit_loss(self, userdata):
        # testdata = {"totalCasinoBet": 700,
        #             "totalCasinoWin": 0,
        #             "totalCustomBet": None,
        #             "totalCustomWin": None,
        #             "totalSportBookBet": None,
        #             "totalSportBookWin": None,
        #             "totalDeposit": 0,
        #             "totalWithdraw": 0,
        #             "totalBonus": None,
        #             "pendingWithdraw": 0,
        #             "rejectedWithdraw": 0 }
        self.action.profit_loss(userdata["token"],testdata=None)

    def test_user_affilated_user_and_all_setelment(self,userdata):
        affiliate = self.action.affiliate_users(userdata["token"])
        aff_comition = self.action.all_settlement(userdata["token"],userdata["user"],affiliate)
        self.action.affiliate_stats(userdata["token"], aff_comition)

    def test_user_logout(self,userdata):
        self.action.logout_user(userdata["token"])