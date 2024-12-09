(ns aoc24.5
  (:require
   [clojure.string :as str]))

(defn read-file [filename]
  (->> filename
       slurp
       (#(str/split % #"\n\s*\n"))  ; Pass string as first argument
       (mapv str/split-lines)))

; returns integer x | y
(defn parse-edge [edge]
  (let [[x y] (str/split (str/trim edge) #"\s*\|\s*")]
    [(Integer/parseInt x) (Integer/parseInt y)]))

; build adj list and track number of ins per node
(defn build-adj-list [edges]
  ; reduce with adj map as the param
  (reduce
   (fn [adj edge-str]
     ; destructure the edge format
     (let [[x y] (parse-edge edge-str)]
      ;;  (println "Processing edge:" x "->" y)
       (update adj x (fnil conj #{}) y)))
   {}
   edges))

(defn make-comparator [order]
  (fn [x y]
    (cond
      ; no order preferecne
      (= x y) 0
      ; x < y
      (and (contains? order x)
           (contains? (get order x) y)) -1
      ; x > y
      (and (contains? order y)
           (contains? (get order y) x)) 1
      :else 0)))

(defn sort-dependency [order adj-list]
  (vec (sort (make-comparator order) adj-list)))

(defn parse-orders [order]
  (let [indiv (str/split order #",")]
    (vec (map Integer/parseInt indiv))))

(defn compare-order1 [before after]
  (if (= before after)
    (nth before (/ (count before) 2))
    0))

(defn compare-order2 [before after]
  (if (= before after)
    0
    (nth after (/ (count after) 2))))

(defn part1_2 [filename]
  (let [files (read-file filename)
        rules (first files)
        orders (map parse-orders (last files))
        adj-list (build-adj-list rules)
        sorter (partial sort-dependency adj-list)
        sorted (map sorter orders)
        calculate1 (map compare-order1 orders sorted)
        calculate2 (map compare-order2 orders sorted)]
    ;; (println "adj list : " adj-list)
    ;; (println "orders : " orders)
    ;; (println "orders[0] : " (nth orders 0))
    ;; (println "sorted[0] : " (sorter (nth orders 0)))
    ;; (println "calculate : " calculate)
    (println "part1 :" (reduce + calculate1))
    (println "part2 :" (reduce + calculate2))))


(part1_2 "5.sample")
(part1_2 "5.input")

