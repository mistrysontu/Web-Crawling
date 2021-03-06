
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ANCHOR BR ELIKE EWATCH LCAST LCOLLECTION LDIRECTORS LLANGUAGE LLIKE LNAME LPRODUCERS LRUNTIME LSTORY LWATCH LWRITERS MCAST MLIKE RA RCAST RLIKE RNAME RRUNTIME RTAG RWATCH SCAST SEP SLIKE STRING SWATCH WSPACEstart : mname\n            | directors\n            | writer\n            | producers\n            | language\n            | cast\n            | story\n            | collection\n            | runtime\n            | similar_movie\n            | watch\n            watch : SWATCH platforms EWATCHplatform : LWATCH string RWATCHplatforms : platform\n                 | platform platformssimilar_movie : SLIKE u_may_like ELIKEsingle_like : LLIKE string MLIKE string RLIKEu_may_like : single_like SEP u_may_like\n                  | single_like\n                  mname : LNAME movie_name RNAMEmovie_name : string SEP string\n                  | string\n                  | string STRING\n     directors : LDIRECTORS celebrity RTAGwriter : LWRITERS celebrity RTAGproducers : LPRODUCERS celebrity RTAGcelebrity : ANCHOR string RAcelebrity : ANCHOR string RA SEP celebrity language : LLANGUAGE string RTAGcast :  SCAST string LCAST string MCAST role RCAST role : stringrole : role SEP stringrole : role BR stringstory : LSTORY temp_story RTAGtemp_story : string\n                  | STRING stories\n                  | temp_story stories\n    stories : STRING string\n              | SEP string\n    collection : LCOLLECTION string RTAGruntime : LRUNTIME time RRUNTIMEtime : STRING string \n            | STRINGstring : STRINGstring : STRING wspaces stringwspaces : WSPACE\n            | WSPACE wspaces'
    
_lr_action_items = {'LNAME':([0,],[13,]),'LDIRECTORS':([0,],[14,]),'LWRITERS':([0,],[15,]),'LPRODUCERS':([0,],[16,]),'LLANGUAGE':([0,],[17,]),'SCAST':([0,],[18,]),'LSTORY':([0,],[19,]),'LCOLLECTION':([0,],[20,]),'LRUNTIME':([0,],[21,]),'SLIKE':([0,],[22,]),'SWATCH':([0,],[23,]),'$end':([1,2,3,4,5,6,7,8,9,10,11,12,45,50,52,53,54,56,61,62,64,67,87,],[0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-20,-24,-25,-26,-29,-34,-40,-41,-16,-12,-30,]),'STRING':([13,17,18,19,20,21,25,26,28,33,34,35,38,41,44,46,48,49,55,57,58,59,60,71,72,75,76,78,81,88,89,],[26,26,26,35,26,38,47,-44,26,58,-35,58,26,26,26,26,26,-46,26,-37,26,26,-36,-45,-47,-38,-39,26,26,26,26,]),'ANCHOR':([14,15,16,80,],[28,28,28,28,]),'LLIKE':([22,65,],[41,41,]),'LWATCH':([23,43,79,],[44,44,-13,]),'RNAME':([24,25,26,47,70,71,],[45,-22,-44,-23,-21,-45,]),'SEP':([25,26,33,34,35,40,57,60,71,73,75,76,84,85,86,90,91,],[46,-44,59,-35,59,65,-37,-36,-45,80,-38,-39,-31,88,-17,-32,-33,]),'RTAG':([26,27,29,30,31,33,34,35,36,57,60,71,73,75,76,83,],[-44,50,52,53,54,56,-35,-44,61,-37,-36,-45,-27,-38,-39,-28,]),'LCAST':([26,32,71,],[-44,55,-45,]),'RA':([26,51,71,],[-44,73,-45,]),'RRUNTIME':([26,37,38,63,71,],[-44,62,-43,-42,-45,]),'MLIKE':([26,66,71,],[-44,78,-45,]),'RWATCH':([26,69,71,],[-44,79,-45,]),'MCAST':([26,71,74,],[-44,-45,81,]),'RLIKE':([26,71,82,],[-44,-45,86,]),'RCAST':([26,71,84,85,90,91,],[-44,-45,-31,87,-32,-33,]),'BR':([26,71,84,85,90,91,],[-44,-45,-31,89,-32,-33,]),'WSPACE':([26,35,49,],[49,49,49,]),'ELIKE':([39,40,77,86,],[64,-19,-18,-17,]),'EWATCH':([42,43,68,79,],[67,-14,-15,-13,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'start':([0,],[1,]),'mname':([0,],[2,]),'directors':([0,],[3,]),'writer':([0,],[4,]),'producers':([0,],[5,]),'language':([0,],[6,]),'cast':([0,],[7,]),'story':([0,],[8,]),'collection':([0,],[9,]),'runtime':([0,],[10,]),'similar_movie':([0,],[11,]),'watch':([0,],[12,]),'movie_name':([13,],[24,]),'string':([13,17,18,19,20,28,38,41,44,46,48,55,58,59,78,81,88,89,],[25,31,32,34,36,51,63,66,69,70,71,74,75,76,82,84,90,91,]),'celebrity':([14,15,16,80,],[27,29,30,83,]),'temp_story':([19,],[33,]),'time':([21,],[37,]),'u_may_like':([22,65,],[39,77,]),'single_like':([22,65,],[40,40,]),'platforms':([23,43,],[42,68,]),'platform':([23,43,],[43,43,]),'wspaces':([26,35,49,],[48,48,72,]),'stories':([33,35,],[57,60,]),'role':([81,],[85,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> mname','start',1,'p_start','20CS60R15_A9_P2.py',198),
  ('start -> directors','start',1,'p_start','20CS60R15_A9_P2.py',199),
  ('start -> writer','start',1,'p_start','20CS60R15_A9_P2.py',200),
  ('start -> producers','start',1,'p_start','20CS60R15_A9_P2.py',201),
  ('start -> language','start',1,'p_start','20CS60R15_A9_P2.py',202),
  ('start -> cast','start',1,'p_start','20CS60R15_A9_P2.py',203),
  ('start -> story','start',1,'p_start','20CS60R15_A9_P2.py',204),
  ('start -> collection','start',1,'p_start','20CS60R15_A9_P2.py',205),
  ('start -> runtime','start',1,'p_start','20CS60R15_A9_P2.py',206),
  ('start -> similar_movie','start',1,'p_start','20CS60R15_A9_P2.py',207),
  ('start -> watch','start',1,'p_start','20CS60R15_A9_P2.py',208),
  ('watch -> SWATCH platforms EWATCH','watch',3,'p_watch','20CS60R15_A9_P2.py',213),
  ('platform -> LWATCH string RWATCH','platform',3,'p_platform','20CS60R15_A9_P2.py',217),
  ('platforms -> platform','platforms',1,'p_platform_multi','20CS60R15_A9_P2.py',221),
  ('platforms -> platform platforms','platforms',2,'p_platform_multi','20CS60R15_A9_P2.py',222),
  ('similar_movie -> SLIKE u_may_like ELIKE','similar_movie',3,'p_similar_movie','20CS60R15_A9_P2.py',232),
  ('single_like -> LLIKE string MLIKE string RLIKE','single_like',5,'p_single_like','20CS60R15_A9_P2.py',236),
  ('u_may_like -> single_like SEP u_may_like','u_may_like',3,'p_like_multi','20CS60R15_A9_P2.py',241),
  ('u_may_like -> single_like','u_may_like',1,'p_like_multi','20CS60R15_A9_P2.py',242),
  ('mname -> LNAME movie_name RNAME','mname',3,'p_mname','20CS60R15_A9_P2.py',250),
  ('movie_name -> string SEP string','movie_name',3,'p_movie_name','20CS60R15_A9_P2.py',254),
  ('movie_name -> string','movie_name',1,'p_movie_name','20CS60R15_A9_P2.py',255),
  ('movie_name -> string STRING','movie_name',2,'p_movie_name','20CS60R15_A9_P2.py',256),
  ('directors -> LDIRECTORS celebrity RTAG','directors',3,'p_directors','20CS60R15_A9_P2.py',266),
  ('writer -> LWRITERS celebrity RTAG','writer',3,'p_writer','20CS60R15_A9_P2.py',271),
  ('producers -> LPRODUCERS celebrity RTAG','producers',3,'p_producers','20CS60R15_A9_P2.py',276),
  ('celebrity -> ANCHOR string RA','celebrity',3,'p_celebrity','20CS60R15_A9_P2.py',280),
  ('celebrity -> ANCHOR string RA SEP celebrity','celebrity',5,'p_multi_celebrity','20CS60R15_A9_P2.py',284),
  ('language -> LLANGUAGE string RTAG','language',3,'p_language','20CS60R15_A9_P2.py',290),
  ('cast -> SCAST string LCAST string MCAST role RCAST','cast',7,'p_cast','20CS60R15_A9_P2.py',296),
  ('role -> string','role',1,'p_cast_role','20CS60R15_A9_P2.py',304),
  ('role -> role SEP string','role',3,'p_cast_roles','20CS60R15_A9_P2.py',308),
  ('role -> role BR string','role',3,'p_cast_roles_multi','20CS60R15_A9_P2.py',312),
  ('story -> LSTORY temp_story RTAG','story',3,'p_story','20CS60R15_A9_P2.py',318),
  ('temp_story -> string','temp_story',1,'p_temp_story','20CS60R15_A9_P2.py',322),
  ('temp_story -> STRING stories','temp_story',2,'p_temp_story','20CS60R15_A9_P2.py',323),
  ('temp_story -> temp_story stories','temp_story',2,'p_temp_story','20CS60R15_A9_P2.py',324),
  ('stories -> STRING string','stories',2,'p_temp_stories','20CS60R15_A9_P2.py',332),
  ('stories -> SEP string','stories',2,'p_temp_stories','20CS60R15_A9_P2.py',333),
  ('collection -> LCOLLECTION string RTAG','collection',3,'p_collection','20CS60R15_A9_P2.py',341),
  ('runtime -> LRUNTIME time RRUNTIME','runtime',3,'p_runtime','20CS60R15_A9_P2.py',347),
  ('time -> STRING string','time',2,'p_time','20CS60R15_A9_P2.py',351),
  ('time -> STRING','time',1,'p_time','20CS60R15_A9_P2.py',352),
  ('string -> STRING','string',1,'p_string_one','20CS60R15_A9_P2.py',361),
  ('string -> STRING wspaces string','string',3,'p_string_multi','20CS60R15_A9_P2.py',366),
  ('wspaces -> WSPACE','wspaces',1,'p_wspaces','20CS60R15_A9_P2.py',370),
  ('wspaces -> WSPACE wspaces','wspaces',2,'p_wspaces','20CS60R15_A9_P2.py',371),
]
