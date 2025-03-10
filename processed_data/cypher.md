MOST DETAILED VIEW:

MATCH (source:NetworkElement)-[r:SENDS_MESSAGE]->(dest:NetworkElement)
WHERE r.step <= 6
MATCH (s1:State)-[t:TRANSITIONS_TO]->(s2:State)
WHERE t.step = r.step
RETURN source, dest, r, s1, s2, t
ORDER BY r.step


STATE MACHINE VIEW:

MATCH (s:State)-[r:TRANSITIONS_TO]->(s2:State)
WHERE r.step <= 6
RETURN s, r, s2
ORDER BY r.step

COMPLETE REGISTRATION FLOW VIEW:

MATCH (s:State)-[r:TRANSITIONS_TO]->(s2:State)
WHERE r.step <= 6
RETURN s, r, s2
ORDER BY r.step


