(ns aoc24.1
  (:require
   [clojure.string :as str]))

(defn read-file [filename]
  (->> (slurp filename)
       str/split-lines
       (map #(str/split % #" "))
       (map #(map str/trim %))
       (map #(filter not-empty %))
       (map #(map (fn [x] (Integer/parseInt x)) %))
       (apply map vector)
       vec))

(defn part1 [filename]
  (let [files (read-file filename)
        x (sort (first files))
        y (sort (last files))
        partitions (partition 2 (interleave x y))]
    (println (reduce + (map (fn [[a b]] (Math/abs (- a b))) partitions)))))

(defn part2 [filename]
  (let [files (read-file filename)
        x (first files)
        y (last files)
        y-freq (frequencies y)]
    (println (reduce + (map (fn [v] (* v (get y-freq v 0))) x)))))

(part1 "1.input")
(part2 "1.input")
