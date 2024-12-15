(ns aoc24.8
  (:require
   [clojure.string :as str]))

(defn read-file [filename]
  (->> filename
       slurp
       str/split-lines))

(defn in-bounds? [grid pos]
  (let [[y x] pos
        height (count grid)
        width (count (first grid))]
    (and (>= y 0) (< y height)
         (>= x 0) (< x width))))

(defn find-positions [grid]
  (->> (for [y (range (count grid))
             x (range (count (first grid)))
             :let [char (get-in grid [y x])]
             :when (not= \. char)]
         [char [y x]])
       (group-by first)
       (map (fn [[k v]] [k (vec (map second v))]))
       (into {})))

(defn calculate-antinode1 [grid positions]
  (let [valid-positions
        (for [pos1 positions
              pos2 positions
              :when (not= pos1 pos2)
              :let [vec (mapv - pos2 pos1)
                    new-pos1 (mapv - pos1 vec)
                    new-pos2 (mapv + pos2 vec)]
              :when (or (in-bounds? grid new-pos1)
                        (in-bounds? grid new-pos2))]
          (filter (partial in-bounds? grid)
                  [new-pos1 new-pos2]))]
    (vec (distinct (mapcat identity valid-positions)))))

(defn positions-in-direction [grid start-pos vec]
  (loop [curr-pos start-pos
         positions []]
    (let [next-pos (mapv + curr-pos vec)]
      (if (in-bounds? grid next-pos)
        (recur next-pos (conj positions next-pos))
        positions))))

(defn all-line-positions [grid pos vec]
  (let [forward (positions-in-direction grid pos vec)
        backward (positions-in-direction grid pos (mapv - vec))]
    (concat backward forward)))

(defn calculate-antinode2 [grid positions]
  (let [valid-positions
        (for [pos1 positions
              pos2 positions
              :when (not= pos1 pos2)
              :let [vec (mapv - pos2 pos1)]
              pos (all-line-positions grid pos1 vec)]
          pos)]
    (vec (distinct valid-positions))))

(defn part1_2 [filename]
  (let [grid (read-file filename)
        positions (find-positions grid)
        antinodes1 (->> positions
                        (map (fn [[_ v]] (calculate-antinode1 grid v)))
                        (mapcat identity)
                        distinct
                        vec)
        antinodes2 (->> positions
                        (map (fn [[_ v]] (calculate-antinode2 grid v)))
                        (mapcat identity)
                        distinct
                        vec)]
    (println antinodes1)
    (println (count antinodes1))
    (println antinodes2)
    (println (count antinodes2))))

;; (part1_2 "8.sample")
(part1_2 "8.input")