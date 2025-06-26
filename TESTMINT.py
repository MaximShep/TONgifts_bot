import asyncio
from pytoniq import WalletV4R2, LiteBalancer
from tonsdk.utils import to_nano, Address

async def transfer_funds(mnemonics_from: list, to_address: str, amount_ton: float, expected_from_address: str, comment: str = "") -> str:
    try:
        provider = LiteBalancer.from_testnet_config(trust_level=1, timeout=10)
        await provider.start_up()

        wallet = await WalletV4R2.from_mnemonic(provider, mnemonics_from)
        
        raw_address = wallet.address.to_str()
        address_obj = Address(raw_address)
        generated_user_friendly = address_obj.to_string(is_user_friendly=True, is_bounceable=False, is_test_only=True)
        generated_raw = address_obj.to_string(is_user_friendly=False, is_bounceable=False)
        generated_bounceable = address_obj.to_string(is_user_friendly=True, is_bounceable=True, is_test_only=True)

        print(f"Ожидаемый адрес: {expected_from_address}")
        print(f"Сгенерированный User-friendly: {generated_user_friendly}")
        print(f"Сгенерированный Raw: {generated_raw}")
        print(f"Сгенерированный Bounceable: {generated_bounceable}")

        if expected_from_address not in [generated_user_friendly, generated_raw, generated_bounceable]:
            await provider.close_all()
            return f"Ошибка: Адреса не совпадают! Проверьте сеть и формат.\nОжидаемый: {expected_from_address}\nСгенерированные:\n - User-friendly: {generated_user_friendly}\n - Raw: {generated_raw}\n - Bounceable: {generated_bounceable}"

        account_state = await provider.get_account_state(wallet.address)
        print(f"Состояние кошелька: {account_state.state.type_}")
        print(f"Баланс кошелька: {account_state.balance / 10**9} TON")

        if account_state.state.type_ == "uninit":
            await provider.close_all()
            return "Ошибка: Кошелек не инициализирован (uninit). Пополните его через Testnet Faucet: https://ton.org/testnet-faucet"

        balance = account_state.balance
        required_amount = to_nano(amount_ton + 0.05, 'ton')
        if balance < required_amount:
            await provider.close_all()
            return f"Ошибка: Недостаточно средств. Баланс: {balance / 10**9} TON, требуется: {amount_ton + 0.05} TON"

        amount_nano = to_nano(amount_ton, 'ton')

        # Минимальный рабочий вызов transfer без комментария
        await wallet.transfer(
            destination=to_address,
            amount=amount_nano
        )

        await provider.close_all()
        return f"Транзакция отправлена. Хэш будет доступен в Testnet Explorer через 1-2 минуты. Адрес отправителя: {generated_user_friendly}"

    except Exception as e:
        await provider.close_all()
        return f"Ошибка при переводе: {str(e)}"

async def main():
    sender_mnemonics = [
        "traffic", "crater", "jump", "grace", "bonus", "object", "tooth", "purse",
        "void", "evil", "join", "unveil", "novel", "boost", "duty", "panther",
        "blossom", "promote", "fish", "excite", "radar", "able", "real", "final"
    ]
    expected_address = "0QDSmflKbS0Nrs4qjFQwmEuq3Z5TDfA6nJS3EVDJYP1N-tcC"
    recipient_address = "0QCsxu2jf0zY3TKyNWLaFsz_S9s_ms-td9NeFxUU_jQdLeWb"
    amount = 0.1
    comment = "Тестовый перевод"  # Оставлен для совместимости, но не используется
    
    result = await transfer_funds(sender_mnemonics, recipient_address, amount, expected_address, comment)
    print(f"Результат: {result}")

if __name__ == "__main__":
    asyncio.run(main())