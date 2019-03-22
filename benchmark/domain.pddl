;; bookshelf domain
;; 

(define (domain bookshelf)
    (:requirements :strips :typing)
    (:types table
            shelf
            slot - sustainable
            workbench
            book
            sustainable - object)
            
    (:predicates (on ?bk - book ?sstnbl - sustainable)
                 (in ?slt - slot ?wrkbch - workbench)
                 (empty ?slt - slot))

    (:action LOAD-WORKBENCH
        :parameters (?bk - book ?tbl - table ?slt - slot)
        :precondition (and (on ?bk ?tbl) (empty ?slt))
        :effect (and (not (on ?bk ?tbl)) (not (empty ?slt)) (on ?bk ?slt)))
    
    (:action LOAD-SHELF
        :parameters (?bk - book ?slt - slot ?shlf - shelf)
        :precondition (on ?bk ?slt)
        :effect (and (not (on ?bk ?slt)) (empty ?slt) (on ?bk ?shlf)))
        
    (:action UNLOAD-WORKBENCH
        :parameters (?bk - book ?tbl - table ?slt - slot)
        :precondition (on ?bk ?slt)
        :effect (and (not (on ?bk ?slt)) (on ?bk ?tbl) (empty ?slt)))
    
    (:action UNLOAD-SHELF
        :parameters (?bk - book ?slt - slot ?shlf - shelf)
        :precondition (and (empty ?slt) (on ?bk ?shlf))
        :effect (and (not (empty ?slt)) (not (on ?bk ?shlf)) (on ?bk ?slt)))
)
