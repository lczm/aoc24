(ns aoc24.4
  (:require
   [clojure.string :as str]))

(defn read-file [filename]
  (->> (slurp filename)
       str/split-lines
       vec))

; get all 4 diagonals from current position
(defn get-diagonals [grid [x y] size]
  (for [dx [-1 1]
        dy [-1 1]
        :let [xs (range x (+ x (* size dx)) dx)
              ys (range y (+ y (* size dy)) dy)]]
    (map #(get-in grid [%2 %1] nil) xs ys)))

(defn get-diagonals-x [grid [x y]]
  [[(get-in grid [(- y 1) (- x 1)] nil)
    (get-in grid [y x] nil)
    (get-in grid [(+ y 1) (+ x 1)] nil)]
   [(get-in grid [(- y 1) (+ x 1)] nil)
    (get-in grid [y x] nil)
    (get-in grid [(+ y 1) (- x 1)] nil)]])

(defn count-xmas [grid]
  (let [height (count grid)
        width (count (first grid))]
    (->> (for [y (range height)
               x (range width)
               :let [horizontal (apply str (take 4 (drop x (nth grid y))))
                     vertical (apply str (map #(get-in grid [% x]) (range y (+ y 4))))
                     reverse-horizontal (apply str (reverse (take 4 (drop x (nth grid y)))))
                     reverse-vertical (apply str (reverse (map #(get-in grid [% x]) (range y (+ y 4)))))
                     diagonals (map #(apply str %) (get-diagonals grid [x y] 4))]]
           (count (filter #(= "XMAS" %) (concat [horizontal vertical reverse-horizontal reverse-vertical] diagonals))))
         (reduce +))))


(defn count-mas [x]
  (= 2 (count (filter #(or (= "MAS" %)
                           (= "SAM" %)) x))))

(defn count-x-mas [grid]
  (let [height (count grid)
        width (count (first grid))]
    (->> (for [y (range height)
               x (range width)
               :let [diagonals (map #(apply str %) (get-diagonals-x grid [x y]))
                     processed-diagonals (count-mas diagonals)]]
           (if processed-diagonals 1 0))
         (reduce +))))

(defn part1 [filename]
  (let [files (read-file filename)]
    (println (count-xmas files))))

(defn part2 [filename]
  (let [files (read-file filename)]
    (println (count-x-mas files))))

(part1 "4.sample")
(part1 "4.input")
(part2 "4.sample")
(part2 "4.input")