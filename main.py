import python_files.setup_workouts as setup_workouts
import python_files.calculate_results as calculate_results
import python_files.consts as consts


def main():
    if consts.SETUPWORKOUTS:
        setup_workouts.setupWorkouts()
    
    calculate_results.calculateWorkouts()

main()
