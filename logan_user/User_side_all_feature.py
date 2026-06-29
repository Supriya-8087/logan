import token
import traceback
from http.client import responses
from urllib import response

import requests
import json

from urllib3.util import url


class User_Side_All_Feature:

    def __init__(self):
        pass

    all_rewards = "https://api-logan.kodedice.com/api/v1/bonus/all-rewards-detail"
    affilaiates_stats = "https://api-logan.kodedice.com/api/v1/user/affiliate-stats"
    profit_loss_url = "https://api-logan.kodedice.com/api/v1/user/profit-loss"
    all_setelments = "https://api-logan.kodedice.com/api/v1/user/all-settlement"
    affilate_user = "https://api-logan.kodedice.com/api/v1/user/affiliate-users"
    providers = "https://api-logan.kodedice.com/api/v1/casino/providers"
    games_settings = "https://api-logan.kodedice.com/api/v1/system/get-game-settings"
    bonus_list = "https://api-logan.kodedice.com/api/v1/bonus/list"
    claimabel_list = "https://api-logan.kodedice.com/api/v1/bonus/claimable-list"
    all_rewards_details = "https://api-logan.kodedice.com/api/v1/bonus/all-rewards-detail"
    send_chat = "https://api-logan.kodedice.com/api/v1/user/chat"
    get_chat = "https://api-logan.kodedice.com/api/v1/user/get-chat?limit=20&startDate=2026-06-19&endDate=2026-06-26&languageId=1&groupId=1"
    signup = "https://api-logan.kodedice.com/api/v1/user/signup"
    login = "https://adminapi-logan.kodedice.com/api/v1/auth/login"

    def login_user(self):
        try:
            print("b")
            payload = {"phoneCode": "+234", "phone": "8010000006", "password": "TestUser@123"}
            response = requests.request("POST", "https://api-logan.kodedice.com/api/v1/user/login", data=payload)
            if response.status_code != 200:
                message = response.json()["message"]
                return message
            else:
                print("Login successful")
                accessToken = response.json()["data"]["accessToken"]
                userdata = response.json()["data"]["user"]
                assert response.status_code == 200
                assert response.json()["data"]["message"] == "User logged in"
                assert userdata["phone"] == "8010000006"
                assert userdata["email"] == "wolf_a@yopmail.com"
                return {"token": accessToken, "userdata": userdata}
        except Exception:
            traceback.print_exc()
            print("error")
            raise

    def login_user_details(self, token, userdata):
        try:
            print(token)
            headers = {"Authorization": f"Bearer {token}".format(token=token)}
            print("headers: ", headers)
            responce = requests.request("GET", "https://api-logan.kodedice.com/api/v1/user/user-detail",
                                        headers=headers)
            if responce.status_code != 200:
                message = responce.json()["errors"]
                print(message[0]["name"])
                assert message[0]["name"] == "InvalidToken"
                return message
            else:
                responce = responce.json()["data"]
                print(responce)
                assert responce["email"] == userdata["email"]
                assert responce["phone"] == userdata["phone"]
                assert responce["fullName"] == userdata["fullName"]
                print("Login successful")
        except Exception:
            traceback.print_exc()
            print("error")
            raise

    def logout_user(self, token):
        try:
            print("b")
            headers = {"Authorization": f"Bearer {token}".format(token=token)}
            print("headers: ", headers)
            responses = requests.request("GET", "https://api-logan.kodedice.com/api/v1/user/logout", headers=headers)
            if responses.status_code != 200:
                return responses.json()
            else:
                assert responses.json()["message"] == "Logout successful"
        except Exception:
            traceback.print_exc()
            print("error")
            raise

    def profit_loss(self, token,testdata):
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.request("GET", self.profit_loss_url,headers=headers)

            if response.status_code != 200:
                message = response.json()["errors"]
                print(message)
                return message
            else:
                response = response.json()
                print(response)
                assert response["errors"] == []
                data = response["data"]
                assert "casinoBets" in data
                assert "totalCasinoWin" in data
                assert "customBets" in data
                assert "totalCustomWin" in data
                assert "sportBets" in data
                assert "totalSportBookWin" in data

                if testdata is not None:
                    assert data["casinoBets"] == testdata["totalCasinoBet"]
                    assert data["totalCasinoWin"] == testdata["totalCasinoWin"]
                    assert data["customBets"] == testdata["totalCustomBet"]
                    assert data["totalCustomWin"] == testdata["totalCustomWin"]
                    assert data["sportBets"] == testdata["totalSportBookBet"]
                    assert data["totalSportBookWin"] == testdata["totalSportBookWin"]
                print("Profit Loss API Validation Successful")
                return data
        except Exception:
            traceback.print_exc()
            print("Profit Loss API Validation Failed")
            raise

    def all_settlement(self,token,userdata,affiliate):
        try:
            headers = {"Authorization": f"Bearer {token}".format(token=token)}
            params = {"limit":10,"page":1}
            response = requests.get("https://api-logan.kodedice.com/api/v1/user/all-settlement", headers=headers,params=params)
            assert response.status_code == 200
            assert response.json()["errors"] == []
            assert response.json()["data"]["count"] == len(response.json()["data"]["rows"])
            data = response.json()["data"]
            print("\n","responce boby:- ",response)
            print("userdata:- ",userdata)
            print("Affiliate: ",affiliate)
            user = affiliate
            for row in data["rows"]:
                assert row["id"] != ""
                assert row["affiliateId"] != ""
                assert row["settlementId"] != ""
                assert row["status"] == "pending"
                assert row["createdAt"] != ""
                assert row["updatedAt"] != ""
                # Affiliate Details
                aff = row["affiliates"]
                assert aff["id"] == row["affiliateId"]
                assert aff["status"] == "ACTIVE"
                assert aff["ownerType"] == "USER"
                # Link with logged-in user
                assert aff["ownerId"] == userdata["id"]
                assert aff["code"] != ""
                assert aff["url"].endswith(aff["code"])

                assert aff["createdAt"] != ""
                assert aff["updatedAt"] != ""
                assert aff["deletedAt"] is None

                # Affiliate Users API validation
            assert affiliate["totalAffiliatedCount"] == data["count"]

            for user in affiliate["affiliateUsers"]:
                assert user["id"] != ""
                assert user["userName"] != ""
                assert user["email"] != ""
                assert "@yopmail.com" in user["email"]
                assert user["active"] is True
                assert user["createdAt"] != ""
            total_profit = 0
            total_wagered = 0

            for row in data["rows"]:
                total_profit += float(row["profitCommisionAmount"])
                total_wagered += float(row["wageredCommisionAmount"])

            return {
                "profit_commission": total_profit,
                "wagered_commission": total_wagered
            }
        except Exception:
            print("All Settlement failed")
            raise

    def affiliate_users(self,token):
        try:
            headers = {"Authorization": f"Bearer {token}".format(token=token)}
            params = {"limit":10,"page":1}
            response = requests.get("https://api-logan.kodedice.com/api/v1/user/affiliate-users", headers=headers,params=params)
            assert response.status_code == 200
            assert response.json()["errors"] == []
            assert response.json()["data"]["totalAffiliatedCount"] == len(response.json()["data"]["affiliateUsers"])
            response = response.json()["data"]
            for user in response["affiliateUsers"]:
                assert user["id"] is not None
                assert user["userName"] != ""
                assert user["email"] != ""
                assert "@yopmail.com" in user["email"]
                assert user["active"] == True
                assert user["createdAt"] != ""
            return response
        except Exception:
            traceback.print_exc()
            return

    def bonus_list(self,bonus_test_data):
        try:
            headers = {"Authorization": f"Bearer {token}".format(token=token)}
            response = requests.post("https://api-logan.kodedice.com/api/v1/user/all-settlement", headers=headers)
            response = response.json()["data"]
            assert response["errors"] == []
            bonus_list = response["data"]["bonuses"]
            assert len(bonus_list) > 0

            for expected_bonus in bonus_test_data:
                actual_bonus = next(
                    (b for b in bonus_list if b["bonusType"] == expected_bonus["bonusType"]),
                    None
                )
                assert actual_bonus is not None
                assert actual_bonus["promotionTitle"] == expected_bonus["promotionTitle"]
                assert actual_bonus["description"] == expected_bonus["description"]
                assert actual_bonus["termsAndConditions"] == expected_bonus["termsAndConditions"]
                assert actual_bonus["bonusType"] == expected_bonus["bonusType"]
                assert actual_bonus["daysToClear"] == expected_bonus["daysToClear"]
                assert actual_bonus["validFrom"] == expected_bonus["validFrom"]
                assert actual_bonus["validUpto"] == expected_bonus["validUpto"]
                assert actual_bonus["currencyCode"] == expected_bonus["currencyCode"]
                assert actual_bonus["active"] == expected_bonus["active"]
                assert actual_bonus["visibleInPromotions"] == expected_bonus["visibleInPromotions"]
                assert actual_bonus["wageringMultiplier"] == expected_bonus["wageringMultiplier"]
                assert actual_bonus["minDeposit"] == expected_bonus["minDeposit"]
                assert actual_bonus["joiningBonusAmount"] == expected_bonus["joiningBonusAmount"]
                assert actual_bonus["maxDepositBonusAmount"] == expected_bonus["maxDepositBonusAmount"]
                assert actual_bonus["referralBonusAmount"] == expected_bonus["referralBonusAmount"]
                assert actual_bonus["claimedCount"] == expected_bonus["claimedCount"]

                assert actual_bonus["bonusPercent"] == expected_bonus["bonusPercent"]
        except  Exception:
            traceback.print_exc()
            return

    def claimable_list(self,bonus_test_data):
        try:
            headers = {"Authorization": f"Bearer {token}".format(token=token)}
            response = requests.post("https://api-logan.kodedice.com/api/v1/user/all-settlement", headers=headers)
            response = response.json()["data"]
            assert response.status_code == 200
            response = response.json()
            assert response["errors"] == []
            claimable_bonus = response["data"]
            assert len(claimable_bonus) > 0
            for expected_bonus in bonus_test_data:
                actual_bonus = next(
                    (bonus for bonus in claimable_bonus
                     if bonus["bonusType"] == expected_bonus["bonusType"]),
                    None
                )

                assert actual_bonus is not None
                assert actual_bonus["bonusId"] == expected_bonus["id"]
                assert actual_bonus["bonusType"] == expected_bonus["bonusType"]
                assert actual_bonus["promotionTitle"] == expected_bonus["promotionTitle"]
                assert actual_bonus["termsAndConditions"] == expected_bonus["termsAndConditions"]
                assert actual_bonus["description"] == expected_bonus["description"]
                assert actual_bonus["daysToClear"] == expected_bonus["daysToClear"]
                assert actual_bonus["status"] is None
                assert actual_bonus["userBonusId"] is None
                assert actual_bonus["wageringStatus"] is None
                assert actual_bonus["wageredAmount"] == 0
                assert actual_bonus["amountToWager"] == 0
                assert actual_bonus["claimableAmount"] == 0
                assert actual_bonus["startDate"] is None
                assert actual_bonus["endDate"] is None
                assert actual_bonus["endDay"] is None
                assert actual_bonus["order"] > 0
                assert actual_bonus["bonusAmount"] is not None
        except Exception:
            traceback.print_exc()
            return

    def all_rewards(self,token):
        try:
            headers = {
                "Authorization": f"Bearer {token}"
            }
            response = requests.request(
                "GET","https://api-logan.kodedice.com/api/v1/bonus/all-rewards-detail",
                headers=headers
            )
            if response.status_code != 200:
                message = response.json()["errors"]
                print(message)
                return message
            else:
                response = response.json()
                print(response)
                assert response["errors"] == []
                data = response["data"]
                assert data["totalDailyBonus"] == 0
                assert data["totalWeeklyBonus"] == 0
                assert data["totalRewarded"] == 0
                assert data["totalWager"] == 700
                assert data["totalPendingRewards"] == 0
                assert data["totalCashback"] == 0
                assert data["otherBonuses"] == 0
                print("All Rewards Validation Successful")
                return data
        except Exception:
            traceback.print_exc()
            print("All Rewards Validation Failed")
            raise

    def affiliate_stats(self, token,commetion):
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get( "https://api-logan.kodedice.com/api/v1/user/affiliate-stats",headers=headers)
            assert response.status_code == 200
            body = response.json()
            assert body["errors"] == []
            data = body["data"]
            # Static validations
            assert isinstance(data["totalWin"], (int, float))
            assert isinstance(data["totalWagering"], (int, float))
            assert isinstance(data["totalSystemProfit"], (int, float))
            # Cross API validation
            assert data["affiliatesPendingCommision"] == commetion["profit_commission"]
            # Validate types
            assert isinstance(data["affiliatesProfitCommision"], (int, float))
            assert isinstance(data["affiliatesWageredCommision"], (int, float))
            assert data["totalDepositAmount"] is None or isinstance(data["totalDepositAmount"], (int, float))
            assert data["totalWithdrawAmount"] is None or isinstance(data["totalWithdrawAmount"], (int, float))
            print("Affiliate Stats Validation Successful")
            return data
        except Exception:
            traceback.print_exc()
            print("Affiliate Stats Validation Failed")
            raise

    def send_chat(self, token, message):
        try:
            headers = {"Authorization": f"Bearer {token}"}
            payload = {"message": message,"languageId": 1,"groupId": 1}
            response = requests.request("POST","https://api-logan.kodedice.com/api/v1/user/chat",headers=headers,json=payload)
            if response.status_code != 200:
                message = response.json()["errors"]
                print(message)
                return message
            else:
                response = response.json()
                print(response)
                assert response["errors"] == []
                data = response["data"]
                assert data["message"] == "Message sent successfully"
                assert data["isContainOffensiveWord"] == False
                print("Send Chat Validation Successful")
                return data

        except Exception:
            traceback.print_exc()
            print("Send Chat Validation Failed")
            raise

    def deposit_amount(self,token,amount,userdata):
        try:
            payload = {"transactionType":"deposit","amount":f"{amount}".format(amount=amount),"currency":"NGN"}
            headers = {"Authorization": f"Bearer {token}".format(token=token)}
            responce = requests.post("https://api-logan.kodedice.com/api/v1/payment/purchase", headers= headers,json=payload)
            responce = responce.json()["data"]
            print(responce)
            assert responce["status"] == 200
            assert responce["msg"] == "Wallet updated successfully"
            assert responce["data"]["amount"] == "{amount}".format(amount=amount)
            assert responce["data"]["currency"] == "NGN"
            assert responce["data"]["transactionType"] == "deposit"
            assert responce["data"]["userType"] == "USER"
            assert responce["data"]["email"] == "{email}".format(email=userdata["email"])
            assert responce["data"]["fullName"] == "{fullName}".format(fullName=userdata["fullName"])
            assert responce["data"]["id"] == "{id}".format(id=userdata["id"])
        except Exception:
            print("Deposit failed")
            raise

    def withdrawal_amount(self,token,amount,userdata):
        try:
            payload = {"transactionType": "withdrawal", "amount": f"{amount}".format(amount=amount), "currency": "NGN"}
            headers = {"Authorization": f"Bearer {token}".format(token=token)}
            responce = requests.post("https://api-logan.kodedice.com/api/v1/payment/redeem", headers=headers,json=payload)
            responce = responce.json()["data"]
            print(responce)
            assert responce["status"] == 200
            assert responce["msg"] == "Wallet updated successfully"
            assert responce["data"]["amount"] == "{amount}".format(amount=amount)
            assert responce["data"]["currency"] == "NGN"
            assert responce["data"]["transactionType"] == "withdrawal"
            assert responce["data"]["userType"] == "USER"
            assert responce["data"]["email"] == "{email}".format(email=userdata["email"])
            assert responce["data"]["fullName"] == "{fullName}".format(fullName=userdata["fullName"])
            assert responce["data"]["id"] == "{id}".format(id=userdata["id"])
        except Exception:
            print("Deposit failed")
            raise

    def transactions_withdraw(self,token,amount,userdata):
        try:
            headers = {"Authorization": f"Bearer {token}".format(token=token),
                       "apikey": "IntegrationsServiceAPIKey123",
                        "apisecrete": "IntegrationsServiceAPISecrete123",
                        "Accept": "application/json"}
            params = {"filterByTransactionType": "withdrawal","limit":10,"pageNo":1}
            url = "https://integrations-svc-dev.prometteur.in/transaction/viewTransactionList"
            responce = requests.get(url,params =params,headers=headers)
            responce = responce.json()
            print(responce)
            assert responce["status"] == 200
            assert responce["msg"] == "Transaction list fetched successfully"
            assert responce["data"]["transactions"][0]["amount"] == amount
            assert responce["data"]["transactions"][0]["currency"] == "NGN"
            assert responce["data"]["transactions"][0]["transactionType"] == "withdrawal"
            assert responce["data"]["transactions"][0]["userId"] == userdata["id"]
            assert responce["data"]["transactions"][0]["status"] == "completed"
            assert responce["data"]["transactions"][0]["paymentGateway"] == "manual"
        except Exception:
            print("Transaction withdrawal failed")
            raise

    def transaction_deposit(self,token,amount,userdata):
        try:
            url = "https://integrations-svc-dev.prometteur.in/transaction/viewTransactionList"
            headers = {"Authorization": f"Bearer {token}".format(token=token),
                       "apikey": "IntegrationsServiceAPIKey123",
                       "apisecrete": "IntegrationsServiceAPISecrete123",
                       "Accept": "application/json"
                       }
            params = {"filterByTransactionType": "deposit","limit":10,"pageNo":1}
            responce = requests.get(url,params =params,headers=headers)
            responce = responce.json()
            print(responce)
            assert responce["status"] == 200
            assert responce["msg"] == "Transaction list fetched successfully"
            assert responce["data"]["transactions"][0]["amount"] == amount
            assert responce["data"]["transactions"][0]["currency"] == "NGN"
            assert responce["data"]["transactions"][0]["transactionType"] == "deposit"
            assert responce["data"]["transactions"][0]["userId"] == userdata["id"]
            assert responce["data"]["transactions"][0]["status"] == "completed"
            assert responce["data"]["transactions"][0]["paymentGateway"] == "manual"
        except Exception:
            print("Deposit transaction failed")
            raise