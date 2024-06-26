    public static boolean testCase1(){
        List<Subject> subjects = new ArrayList<>();
        Subject subject1 = new Subject();
        subject1.status = false;
        subject1.marks = 0;
        subjects.add(subject1);
        Subject subject2 = new Subject();
        subject2.status = true;
        subject2.marks = 1;
        subjects.add(subject2);
        Subject subject3 = new Subject();
        subject3.status = true;
        subject3.marks = 2;
        subjects.add(subject3);
        Subject subject4 = new Subject();
        subject4.status = false;
        subject4.marks = 3;
        subjects.add(subject4);

        removeFalseSubjects(subjects);

        return !subjects.contains(subject1) && subjects.contains(subject2) && subjects.contains(subject3)
                && !subjects.contains(subject4) && subjects.size() == 2;
    }

    public static void main(String args[]){
        System.out.print(testCase1());
        if(!testCase1()){
            System.exit(-1);
        }

    }
}