import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # Read database file into a variable
    STRs = []
    profiles = []

    with open(sys.argv[1], "r") as f:
        reader = csv.DictReader(f)
        # populate list of STRs
        STRs = reader.fieldnames[1:]
        for row in reader:
            profiles.append(row)
        # print(f"STRs: {STRs} \nprofiles: {profiles}")

    # Initialise dictionary for sequence file
    seq_count = dict.fromkeys(STRs, 0)

    #  Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as f:
        sequence = f.readline()

        # Find longest match of each STR in DNA sequence
        for STR in STRs:
            seq_count[STR] = longest_match(sequence, STR)

        # print(f"seq_count: {seq_count}")

    # Check if any person has same amount of STR repeats as sequence
    for profile in profiles:
        match_count = 0

        for STR in STRs:
            if int(profile[STR]) != seq_count[STR]:
                continue
            else:
                match_count += 1
        # print(f"match count: {match_count}")

        # print(f"lens of STRs: {len(STRs)}")
        if match_count == len(STRs):
            print(profile['name'])
            exit(0)

    print("No match")
    exit(1)

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
