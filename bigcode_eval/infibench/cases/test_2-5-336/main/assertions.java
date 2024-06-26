
    public static boolean testCase1(){
        PriorityQueue queue = createPriorityQueue();

        Pair<Integer, Integer> pair1 = new Pair<>(1, 2436);
        // pair1.key = 1;
        // pair1.value = 2436;

        Pair<Integer, Integer> pair2 = new Pair<>(5, 1034);
        // pair2.key = 5;
        // pair2.value = 1034;

        Pair<Integer, Integer> pair3 = new Pair<>(2, 16);
        // pair3.key = 2;
        // pair3.value = 16;

        Pair<Integer, Integer> pair4 = new Pair<>(4, 187);
        // pair4.key = 4;
        // pair4.value = 187;

        Pair<Integer, Integer> pair5 = new Pair<>(3, 2);
        // pair5.key = 3;
        // pair5.value = 2;

        queue.add(pair1);
        queue.add(pair2);
        queue.add(pair3);
        queue.add(pair4);
        queue.add(pair5);

        if(queue.poll() != pair1){
            return false;
        }
        if(queue.poll() != pair3){
            return false;
        }
        if(queue.poll() != pair5){
            return false;
        }
        if(queue.poll() != pair4){
            return false;
        }
        if(queue.poll() != pair2){
            return false;
        }
        return true;
    }

    public static void main(String args[]){
        System.out.println(testCase1());
        if(!testCase1()){
            System.exit(-1);
        }
    }
}