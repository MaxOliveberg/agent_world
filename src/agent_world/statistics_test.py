from src.agent_world.statistics.statistics import initialise_statistics, statistics_manager

if __name__ == "__main__":
    # Todo: This is not a real clock_tests, write real clock_tests!
    initialise_statistics()
    for i in range(10):
        statistics_manager.log({"name": "Max", "age": i})
        statistics_manager.log({"name": "Paul", "age": i})
    print(statistics_manager.query_values(["Max"]))
