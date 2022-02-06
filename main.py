import python_files.setup_workouts as setup_workouts
import python_files.calculate_results as calculate_results
import python_files.consts as consts
import python_files.shared as shared
import python_files.change_team_category as change_team_category
import python_files.sanitize_teams as sanitize_teams
import python_files.sanitize_results as sanitize_results


def main():
    print("1: Setup workouts based on settings")
    print("2: Calculate workout results based on inputs")
    print("3: Sanitize results")
    if shared.isTeamCompetition():
        print("4: Change team's category")
    if shared.isTeamCompetition():
        print("5: Sanitize team names")
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

    if val == '3':
        sanitize_results.sanitizeResults()

    if shared.isTeamCompetition() and val == '4':
        change_team_category.changeTeams()

    if shared.isTeamCompetition() and val == '5':
        sanitize_teams.sanitizeTeams()


main()
