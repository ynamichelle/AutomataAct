package CcommentAct;

import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;

public class Ccomment {

    // Simulates the NFA using a set of active states
    public static boolean runNFA(String input) {
        // Initial state set: starts with { q0 }
        Set<Integer> currentStates = new HashSet<>();
        currentStates.add(0);

        for (int i = 0; i < input.length(); i++) {
            char ch = input.charAt(i);
            
            // Map any character other than '*' or '/' to placeholder 'a'
            char symbol = (ch == '*' || ch == '/') ? ch : 'a';
            Set<Integer> nextStates = new HashSet<>();

            for (int state : currentStates) {
                switch (state) {
                    case 0: // q0
                        if (symbol == '/') nextStates.add(1);
                        break;

                    case 1: // q1
                        if (symbol == '*') nextStates.add(2);
                        break;

                    case 2: // q2 (Inside comment body)
                        // Loops on all symbols; non-deterministically branches on '*' to q3
                        nextStates.add(2);
                        if (symbol == '*') nextStates.add(3);
                        break;

                    case 3: // q3 (Saw closing '*')
                        if (symbol == '/') nextStates.add(4);
                        break;

                    case 4: // q4 (Accepting state)
                        // No outgoing transitions; extra characters terminate branch
                        break;
                }
            }

            currentStates = nextStates;
            if (currentStates.isEmpty()) {
                return false;
            }
        }

        // Accept if accepting state q4 is active at the end of the input
        return currentStates.contains(4);
    }

    public static void main(String[] args) {
        // Test cases from the lecture slide
        Map<String, String> testCases = new LinkedHashMap<>();
        testCases.put("/*a*/", "Expected: Accepted");
        testCases.put("/**/", "Expected: Accepted");
        testCases.put("/***/", "Expected: Accepted");
        testCases.put("/*aaa*aaa*/", "Expected: Accepted");
        testCases.put("/*a/a*/", "Expected: Accepted");

        testCases.put("/**", "Expected: Rejected");
        testCases.put("/**/a/*aa*/", "Expected: Rejected");
        testCases.put("aaa/**/a", "Expected: Rejected");
        testCases.put("/*/", "Expected: Rejected");
        testCases.put("/**a/", "Expected: Rejected");
        testCases.put("//aaaa", "Expected: Rejected");

        System.out.println("==================================================");
        System.out.println("       NFA C-STYLE COMMENT VALIDATOR (JAVA)       ");
        System.out.println("==================================================\n");

        System.out.printf("%-18s | %-10s | %s%n", "Input String", "Result", "Evaluation");
        System.out.println("--------------------------------------------------");

        for (Map.Entry<String, String> entry : testCases.entrySet()) {
            boolean isAccepted = runNFA(entry.getKey());
            String status = isAccepted ? "ACCEPTED" : "REJECTED";
            System.out.printf("%-18s | %-10s | %s%n", entry.getKey(), status, entry.getValue());
        }

        System.out.println("\n==================================================");
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter your own string to test: ");
        if (scanner.hasNextLine()) {
            String userInput = scanner.nextLine();
            boolean userResult = runNFA(userInput);
            System.out.println("Input: \"" + userInput + "\" -> Status: " + (userResult ? "ACCEPTED" : "REJECTED"));
        }
        scanner.close();
    }
}