(ns aoc24.6
  (:require
   [clojure.string :as str]))

(defn read-file [filename]
  (->> filename
       slurp
       str/split-lines))

(defn out-of-grid? [[x y] width height]
  (or (< x 0)
      (> x (- width 1))
      (< y 0)
      (> y (- height 1))))

(defn get-starting-pos [grid width height]
  (first
   (for [row (range width)
         col (range height)
         :when (= (get-in grid [row col]) \^)]
     [row col])))

(defn direction-turn [direction]
  (cond
    (= direction [-1 0]) [0 1]
    (= direction [0 1]) [1 0]
    (= direction [1 0]) [0 -1]
    (= direction [0 -1]) [-1 0]))

(defn traverse [grid position direction visited]
  (if (out-of-grid? position (count (first grid)) (count grid))
    visited
    (let [next-pos (mapv + position direction)
          next-grid (get-in grid next-pos)]
      ;; (println "Adding : " position)
      (if (contains? visited [position direction])
        []
        (if (= next-grid \#)
          ; turn right
          (recur grid position (direction-turn direction) (conj visited [position direction]))
          (recur grid (mapv + position direction) direction (conj visited [position direction])))))))

(defn update-grid [grid [row col] new]
  (let [old-row (nth grid row)
        updated-row (str (apply str (assoc (vec old-row) col new)))]
    (assoc grid row updated-row)))

(defn find-blockers [grid position direction available]
  (reduce (fn [acc available-position]
            (let [updated-grid (update-grid grid (first available-position) "#")
                  x (traverse updated-grid position direction (set nil))]
              (if (= (count x) 0)
                (conj acc (first available-position))
                acc)))
          #{} available))

(defn part1 [filename]
  (let [grid (read-file filename)
        start (get-starting-pos grid (count (first grid)) (count grid))
        positions (traverse grid start [-1 0] (set nil))
        blockers (find-blockers grid start [-1 0] positions)]
    (println (count positions))
    (println (count blockers))))

;; (part1 "6.sample")
(part1 "6.input")