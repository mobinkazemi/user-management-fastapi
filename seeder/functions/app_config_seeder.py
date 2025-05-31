from userConfig.repository import UserConfigRepository

userConfigRepo = UserConfigRepository()


def user_config_seeder():
    currentConfigs = userConfigRepo.findAll()

    if currentConfigs:
        print("UserConfig already exists, skipping seeder.")
        return
    print("Creating UserConfig...")
    userConfigRepo.createOne({"expirePasswordDays": 90, "passwordAdvantageDays": 3})
