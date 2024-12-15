(ns aoc24.7
  (:require
   [clojure.string :as str]))

; note to use bigint instead of Integer/parseInt
; since Integer/parseInt has a limit of 2bil
; and the input can get really big
(defn read-file [filename]
  (->> filename
       slurp
       str/split-lines
       (map (fn [line]
              (let [[id nums] (str/split line #": ")]
                [(bigint (read-string id))
                 (->> (str/split nums #" ")
                      (map #(bigint (read-string %))))])))))

(defn evaluate [sequence ops]
  (let [result (reduce (fn [acc [op n]]
                         (case op
                           \+ (+ acc n)
                           \* (* acc n)
                           \| (bigint (str acc n))))
                       (first sequence)
                       (map vector ops (rest sequence)))]
    ;; (println "Evaluating" sequence "with ops" ops "=" result)
    result))

(defn generate-permutations [length]
  (if (zero? length)
    '("")
    (for [prev-perm (generate-permutations (dec length))
          char ["+", "*"]]
      (str prev-perm char))))

(defn generate-permutations2 [length]
  (if (zero? length)
    '("")
    (for [prev-perm (generate-permutations2 (dec length))
          char ["+", "*", "|"]]
      (str prev-perm char))))

(println (generate-permutations2 5))

(defn attempt1 [[final sequence]]
  (let [ops (generate-permutations (dec (count sequence)))]
    (some (fn [op-seq]
            (= final (evaluate sequence op-seq)))
          ops)))

(defn attempt2 [[final sequence]]
  (let [ops (generate-permutations2 (dec (count sequence)))]
    (some (fn [op-seq]
            (= final (evaluate sequence op-seq)))
          ops)))

(defn part1_2 [filename]
  (let [file (read-file filename)
        answer1 (->> file
                     (filter attempt1)
                     (map first)
                     (reduce +))
        answer2 (->> file
                     (filter attempt2)
                     (map first)
                     (reduce +))]
    (println answer1)
    (println answer2)))

;; (part1_2 "7.sample")
(part1_2 "7.input")
