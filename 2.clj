(ns aoc24.2
  (:require
   [clojure.string :as str]))

(defn read-file [filename]
  (->> (slurp filename)
       str/split-lines
       (map #(str/split % #" "))
       (map #(map str/trim %))
       (map #(filter not-empty %))
       (map #(map (fn [x] (Integer/parseInt x)) %))
       vec))

(defn is-safe? [compare-fn min-diff max-diff numbers]
  (every? (fn [[a b]]
            (let [diff (Math/abs (- a b))]
              (and (compare-fn a b)
                   (<= min-diff diff)
                   (<= diff max-diff))))
          (partition 2 1 numbers)))

(defn get-all-possibilities [numbers]
  (map vec
       (for [i (range (count numbers))]
         (concat (take i numbers) (drop (inc i) numbers)))))

(defn part1_2 [filename]
  (let [files (read-file filename)
        is-safe-ascending? (partial is-safe? < 1 3)
        is-safe-descending? (partial is-safe? > 1 3)
        check-any-safe (fn [predicate sequences]
                         (some true? (map predicate sequences)))
        check-any-ascending (partial check-any-safe is-safe-ascending?)
        check-any-descending (partial check-any-safe is-safe-descending?)
        x (map is-safe-ascending? files)
        y (map is-safe-descending? files)
        possibilites (map get-all-possibilities files)
        xx (map check-any-ascending possibilites)
        yy (map check-any-descending possibilites)]
    ;; (println xx)
    ;; (println yy)
    (println (count (filter true? (map (fn [x y] (or x y)) x y))))
    (println (count (filter true? (map (fn [x y] (or x y)) xx yy))))))

;; (part1_2 "2.sample")
(part1_2 "2.input")
