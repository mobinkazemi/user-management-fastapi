from appConfig.repository import AppConfigRepository

appConfigRepo = AppConfigRepository()


def app_config_seeder():
    currentConfigs = appConfigRepo.findAll()

    if currentConfigs:
        print("AppConfig already exists, skipping seeder.")
        return
    print("Creating AppConfig...")
    appConfigRepo.createOne({"expirePasswordDays": 90, "passwordAdvantageDays": 3})
