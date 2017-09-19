WordChoice


the dog barked loudly at the mailman
['the,dog           ', 'dog,barked        ', 'barked,loudly     ', 'loudly,at         ', 'at,the            ', 'the,mailman       ']
[0.056649426038716012, 0.34046032280900662, 0.43073733965486516, 0.11958903950439942, 0.32383936092102278, -0.010017586518783997]
 
the man barked nails at the wood
['the,man           ', 'man,barked        ', 'barked,nails      ', 'nails,at          ', 'at,the            ', 'the,wood          ']
[0.13924067067349327, 0.081682517880380945, 0.20281009137477546, 0.050926967937640392, 0.32383936092102278, 0.1170524727561856]
 
the dog hammered loudly into mailman
['the,dog           ', 'dog,hammered      ', 'hammered,loudly   ', 'loudly,into       ', 'into,mailman      ']
[0.056649426038716012, -0.018577151899979875, 0.12202856729023488, 0.099676897569367803, 0.013864047193085564]
 
the man hammered nails into wood
['the,man           ', 'man,hammered      ', 'hammered,nails    ', 'nails,into        ', 'into,wood         ']
[0.13924067067349327, 0.071761166629866147, 0.20719839402476867, 0.023759452133699968, 0.078167382884640119]




## WORDCHOICE SUGGESTION:
See man -vs- worker -vs- builder

Currently only consecutive, but can also use "skip-1" word and evaluate as well - in the same sentence.
There should be a mathmatical way to determine the closest vector to two vectors. Perhaps for three + more as well.


['the,man           ', 'man,hammered      ', 'hammered,nails    ', 'nails,into        ', 'into,wood         ']
[0.13924067067349327, 0.071761166629866147, 0.20719839402476867, 0.023759452133699968, 0.078167382884640119]

the worker hammered nails into wood
['the,worker        ', 'worker,hammered   ', 'hammered,nails    ', 'nails,into        ', 'into,wood         ']
[0.01417872092041526, 0.087302291097278259, 0.20719839402476867, 0.023759452133699968, 0.078167382884640119]

the builder hammered nails into wood
['the,builder       ', 'builder,hammered  ', 'hammered,nails    ', 'nails,into        ', 'into,wood         ']
[0.11558593978215768, 0.18800232375286965, 0.20719839402476867, 0.023759452133699968, 0.078167382884640119]