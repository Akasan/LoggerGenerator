from LoggerGenerator import logger_gen
from Function import func

logger_gen(globals())


if __name__ == "__main__":
    log.info("Start")
    func()
    log.info("End")
