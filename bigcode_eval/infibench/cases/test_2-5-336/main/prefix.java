// package main;
import java.util.*;

public class Main
{
    public static class Pair<T,U> {
        private final T key;
        private final U value;

        public Pair(T key, U value) {
            this.key = key;
            this.value = value;
        }

        public T getKey() {
            return this.key;
        }

        public U getValue() {
            return this.value;
        }
    }
