import requests
from config import Config
import re
import logging
import asyncio
from pytoniq import WalletV3R2, LiteBalancer  # Можно заменить на WalletV3R1, WalletV3R2, WalletV4R1 WalletV4R2
from tonsdk.utils import to_nano, Address
from database.repository import update_address_buyer, check_refund_exists, create_refund, update_deal_status


class TonService:
    def __init__(self):
        self.base_url = "https://tonapi.io/v2/"
        self.headers = {
            "Authorization": f"Bearer {Config.TONAPI_TOKEN}",
            "Content-Type": "application/json"
        }
        self.provider = None

    async def initialize(self):
        """Инициализация LiteBalancer при старте бота"""
        self.provider = LiteBalancer.from_mainnet_config()
        await self.provider.start_up()

    async def check_payment(self, hex_id: str, expected_ton: float) -> bool:
        # return True
        expected_amount = int(expected_ton * 10 ** 9)  # Переводим TON в нанотоны
        print("Проверка платежа для HEX:", hex_id)
        url = f"https://tonapi.io/v2/blockchain/accounts/{Config.ADMIN_TON_ADDRESS}/transactions"

        try:
            response = requests.get(
                url,
                headers={"Authorization": f"Bearer {Config.TONAPI_TOKEN}"},
                params={"limit": 150}
            )
            if response.status_code != 200:
                print(f"Ошибка TonAPI: {response.status_code}")
                return False

            transactions = response.json().get("transactions", [])
            pattern = re.compile(rf"DEAL_{hex_id}|deal\s*#{hex_id}", re.IGNORECASE)

            # Сначала ищем платежи с корректным комментарием и суммой
            for tx in transactions:
                in_msg = tx.get("in_msg", {})
                amount = in_msg.get("value", 0)
                comment = in_msg.get("decoded_body", {}).get("text", "")
                buyer_address = in_msg.get("source", {}).get("address", "")

                if pattern.search(comment) and amount == expected_amount:
                    print(f"✅ Платеж найден: {tx['hash']}, сумма: {amount / 10 ** 9} TON")
                    update_address_buyer(hex_id, buyer_address)
                    return True

            # Проверяем платежи с верным комментарием, но НЕВЕРНОЙ СУММОЙ
            for tx in transactions:
                in_msg = tx.get("in_msg", {})
                idshnik = in_msg.get("hash", "")
                fee = in_msg.get("fwd_fee", 0)
                amount = in_msg.get("value", 0)
                comment = in_msg.get("decoded_body", {}).get("text", "")
                buyer_address = in_msg.get("source", {}).get("address", "")


                if pattern.search(comment) and amount < expected_amount:
                    print(f"⚠️ Недостаточная сумма: {amount / 10 ** 9} TON вместо {expected_ton}")
                    if not check_refund_exists(idshnik):
                        create_refund(
                            deal_id=idshnik,
                            wallet_address=buyer_address,
                            refund_amount=((amount / 10 ** 9)-(fee/10**9)),
                        )
                        await self.refund_payment(buyer_address, ((amount / 10 ** 9)-(fee/10**9)))  # Возвращаем полученную сумму
                        update_deal_status(hex_id, "refunded_because_scam")
                        print(f"🔄 Автоматический возврат {((amount / 10 ** 9)-(fee/10**9))} TON на {buyer_address}")
                    else:
                        print('Платеж уже был возвращен')
                    return False

            # Проверяем платежи с верным комментарием, но БОЛЬШЕЙ СУММОЙ
            for tx in transactions:
                in_msg = tx.get("in_msg", {})
                idshnik = in_msg.get("hash", "")
                fee = in_msg.get("fwd_fee", 0)
                amount = in_msg.get("value", 0)
                comment = in_msg.get("decoded_body", {}).get("text", "")
                buyer_address = in_msg.get("source", {}).get("address", "")

                if pattern.search(comment) and amount > expected_amount:
                    print(f"⚠️ Сумма больше. Переведено: {amount / 10 ** 9} TON вместо {expected_ton}")
                    if not check_refund_exists(idshnik):
                        create_refund(
                            deal_id=idshnik,
                            wallet_address=buyer_address,
                            refund_amount=((amount / 10 ** 9) - expected_ton - (fee / 10 ** 9)),
                        )
                        await self.refund_payment(buyer_address, (
                                    (amount / 10 ** 9) -expected_ton- (fee / 10 ** 9)))  # Возвращаем полученную сумму
                        update_deal_status(hex_id, "refunded_because_scam")
                        print(
                            f"🔄 Автоматический возврат {((amount / 10 ** 9) - expected_ton - (fee / 10 ** 9))} TON на {buyer_address}")
                    else:
                        print('Платеж уже был возвращен')
                    return True

            # Проверяем платежи без комментария
            for tx in transactions:
                in_msg = tx.get("in_msg", {})
                idshnik = in_msg.get("hash", "")
                fee = in_msg.get("fwd_fee", 0)
                amount = in_msg.get("value", 0)
                buyer_address = in_msg.get("source", {}).get("address", "")
                comment = in_msg.get("decoded_body", {}).get("text", "")

                if not comment.strip() and amount == expected_amount:
                    if not check_refund_exists(idshnik):
                        create_refund(
                            deal_id=idshnik,
                            wallet_address=buyer_address,
                            refund_amount=((amount / 10 ** 9)-(fee/10**9)),
                        )
                        await self.refund_payment(buyer_address, ((amount / 10 ** 9)-(fee/10**9)))  # Возвращаем полученную сумму
                        print(f"🔄 Автоматический возврат {((amount / 10 ** 9)-(fee/10**9))} TON на {buyer_address}")
                    return False

            print("❌ Платеж не найден или сумма не совпадает")
            return False

        except Exception as e:
            print(f"❗ Критическая ошибка: {e}")
            return False

    # def check_payment(self, hex_id: str, expected_ton: float) -> bool:
    #     # return True
    #     expected_amount = int(expected_ton * 10**9)  # Переводим TON в нанотоны
    #     print("Проверка платежа для HEX:", hex_id)
    #     url = f"https://tonapi.io/v2/blockchain/accounts/{Config.ADMIN_TON_ADDRESS}/transactions"
    #     try:
    #         response = requests.get(
    #             url,
    #             headers={"Authorization": f"Bearer {Config.TONAPI_TOKEN}"},
    #             params={"limit": 150}
    #         )
    #         if response.status_code != 200:
    #             print(f"Ошибка TonAPI: {response.status_code}")
    #             return False
    #
    #         transactions = response.json().get("transactions", [])
    #         pattern = re.compile(rf"DEAL_{hex_id}|deal\s*#{hex_id}", re.IGNORECASE)
    #
    #         for tx in transactions:
    #             buyer_adress=tx.get("in_msg", {}).get("source", {}).get("address", "")
    #             comment = tx.get("in_msg", {}).get("decoded_body", {}).get("text", "")
    #             amount = tx.get("in_msg", {}).get("value", 0)
    #
    #             if pattern.search(comment) and amount == expected_amount:
    #                 print(f"Платеж найден: {tx['hash']}, сумма: {amount/10**9} TON")
    #                 update_address_buyer(hex_id, buyer_adress)
    #                 return True
    #             elif pattern.search(comment):
    #                 print(f"Найден комментарий, но неверная сумма: {amount/10**9} TON вместо {expected_ton}")
    #
    #         print("Платеж не найден или сумма не совпадает")
    #         return False
    #     except Exception as e:
    #         print(f"Критическая ошибка: {e}")
    #         return False

    async def transfer_funds(self, to_address: str, amount_ton: float, deal_id: str) -> bool:
        # return True
        try:
            provider = LiteBalancer.from_mainnet_config(trust_level=1, timeout=10)
            await provider.start_up()

            # mnemonics_from = Config.MNEMONICS
            wallet = await WalletV3R2.from_mnemonic(provider,
                                                    Config.MNEMONICS)  # Попробуйте WalletV3R2 или другие версии

            raw_address = wallet.address.to_str()
            address_obj = Address(raw_address)
            generated_user_friendly = address_obj.to_string(is_user_friendly=True, is_bounceable=False)
            generated_raw = address_obj.to_string(is_user_friendly=False, is_bounceable=False)
            generated_bounceable = address_obj.to_string(is_user_friendly=True, is_bounceable=True)

            print(f"Сгенерированный User-friendly: {generated_user_friendly}")
            print(f"Сгенерированный Raw: {generated_raw}")
            print(f"Сгенерированный Bounceable: {generated_bounceable}")

            account_state = await provider.get_account_state(wallet.address)
            print(f"Состояние кошелька: {account_state.state.type_}")
            print(f"Баланс кошелька: {account_state.balance / 10 ** 9} TON")

            if account_state.state.type_ == "uninit":
                await provider.close_all()
                print("Ошибка: Кошелек не инициализирован (uninit). Пополните его через биржу или кошелек TON.")
                return False

            balance = account_state.balance
            required_amount = to_nano(amount_ton, 'ton')
            if balance < required_amount:
                await provider.close_all()
                print(f"Ошибка: Недостаточно средств. Баланс: {balance / 10 ** 9} TON, требуется: {amount_ton} TON")
                return False
            amount_nano = to_nano(amount_ton, 'ton')

            await wallet.transfer(
                destination=to_address,
                amount=amount_nano,
                body = deal_id
            )

            await provider.close_all()
            print(
                f"Транзакция отправлена. Хэш будет доступен в TON Explorer через 1-2 минуты. Адрес отправителя: {generated_user_friendly}")
            return True

        except Exception as e:
            await provider.close_all()
            print(f"Ошибка при переводе: {str(e)}")
            return False

    async def refund_payment(self, to_address: int, amount_ton: float):
        try:
            provider = LiteBalancer.from_mainnet_config(trust_level=1, timeout=10)
            await provider.start_up()

            # mnemonics_from = Config.MNEMONICS
            wallet = await WalletV3R2.from_mnemonic(provider,
                                                    Config.MNEMONICS)  # Попробуйте WalletV3R2 или другие версии

            raw_address = wallet.address.to_str()
            address_obj = Address(raw_address)
            generated_user_friendly = address_obj.to_string(is_user_friendly=True, is_bounceable=False)
            generated_raw = address_obj.to_string(is_user_friendly=False, is_bounceable=False)
            generated_bounceable = address_obj.to_string(is_user_friendly=True, is_bounceable=True)

            print(f"Сгенерированный User-friendly: {generated_user_friendly}")
            print(f"Сгенерированный Raw: {generated_raw}")
            print(f"Сгенерированный Bounceable: {generated_bounceable}")

            account_state = await provider.get_account_state(wallet.address)
            print(f"Состояние кошелька: {account_state.state.type_}")
            print(f"Баланс кошелька: {account_state.balance / 10 ** 9} TON")

            if account_state.state.type_ == "uninit":
                await provider.close_all()
                print("Ошибка: Кошелек не инициализирован (uninit). Пополните его через биржу или кошелек TON.")
                return False

            balance = account_state.balance
            required_amount = to_nano(amount_ton, 'ton')
            if balance < required_amount:
                await provider.close_all()
                print(f"Ошибка: Недостаточно средств. Баланс: {balance / 10 ** 9} TON, требуется: {amount_ton} TON")
                return False
            amount_nano = to_nano(amount_ton, 'ton')

            await wallet.transfer(
                destination=to_address,
                amount=amount_nano
            )

            await provider.close_all()
            print(
                f"Транзакция отправлена. Хэш будет доступен в TON Explorer через 1-2 минуты. Адрес отправителя: {generated_user_friendly}")
            return True

        except Exception as e:
            await provider.close_all()
            print(f"Ошибка при переводе: {str(e)}")
            return False