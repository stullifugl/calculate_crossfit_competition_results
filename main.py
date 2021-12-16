import python_files.setup_workouts as setup_workouts
import python_files.calculate_results as calculate_results
import python_files.consts as consts
import python_files.shared as shared
import python_files.change_team_category as change_team_category

def main():
    print("1: Setup workouts based on settings")
    print("2: Calculate workout results based on inputs")
    if shared.isTeamCompetition():
        print("3: Change team's category")
    val = input("Choose what you wish to do: ")

    if val == '1':
        if consts.SETUPWORKOUTS == False:
            print("Setting up workouts is disabled in consts, change and run again")
        else:
            if consts.ADDRANDOMSCORES:
                print("Random scores will be added to the workouts")
            setup_workouts.setupWorkouts()

    if val == '2':
        calculate_results.calculateWorkouts()

    if shared.isTeamCompetition() and val == '3':
        change_team_category.changeTeams()

main()
