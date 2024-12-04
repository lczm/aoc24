(ns aoc24.3
  (:require
   [clojure.string :as str]))

(defn read-file [filename]
  (->> (slurp filename)
       str/split-lines
       vec))

(defn extract-muls [s]
  (->> (re-seq #"mul\(\d+,\d+\)" s)
       (filter some?)
       vec))

(defn extract-muls-do-donts [s]
  (->> (re-seq #"mul\(\d+,\d+\)|do\(\)|don't\(\)" s)
       (filter some?)
       vec))

(defn parse-mul [[x y]]
  (map #(Integer/parseInt %) [x y]))

(defn filter-donts [collection]
  (loop [[x & xs] collection
         output []
         collecting? true]
    (if (nil? x)
      output
      (cond
        (= x "don't()") (recur xs output false)
        (= x "do()") (recur xs output true)
        :else (if collecting?
                (recur xs (conj output x) collecting?)
                (recur xs output collecting?))))))

(defn solve1 [s]
  (->> (extract-muls s)
       (map #(re-seq #"\d+" %))
       (map parse-mul)
       (map #(apply * %))
       (reduce +)))

(defn solve2 [s]
  (->> (extract-muls-do-donts s)
       filter-donts
       (map #(re-seq #"\d+" %))
       (map parse-mul)
       (map #(apply * %))
       (reduce +)))

(defn part1 [filename]
  (let [files (read-file filename)
        files (map solve1 files)]
    (println (reduce + files))))

(defn part2 [filename]
  (let [files (read-file filename)]
    (println (solve2 (str/join "" files)))))

(part1 "3.sample")
(part1 "3.input")
(part2 "3.sample2")
(part2 "3.input")
