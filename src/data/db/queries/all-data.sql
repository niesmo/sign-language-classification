SELECT 
  a.id,
  a.lable,
  a.hand_sphere_radius,
   
  b.x 'palm_position_x', 
  b.y 'palm_position_y', 
  b.z 'palm_position_z', 

  c.x 'palm_direction_x', 
  c.y 'palm_direction_y', 
  c.z 'palm_direction_z', 

  d.x 'palm_normal_direction_x', 
  d.y 'palm_normal_direction_y', 
  d.z 'palm_normal_direction_z', 

  e.x 'wrist_position_x', 
  e.y 'wrist_position_y', 
  e.z 'wrist_position_z', 

  g.x 'thumb_tip_position_x', 
  g.y 'thumb_tip_position_y', 
  g.z 'thumb_tip_position_z', 

  h.x 'thumb_metacarpal_position_x', 
  h.y 'thumb_metacarpal_position_y', 
  h.z 'thumb_metacarpal_position_z', 

  i.x 'thumb_proximal_position_x', 
  i.y 'thumb_proximal_position_y', 
  i.z 'thumb_proximal_position_z', 

  j.x 'thumb_intermediate_position_x', 
  j.y 'thumb_intermediate_position_y', 
  j.z 'thumb_intermediate_position_z', 

  k.x 'thumb_distal_position_x', 
  k.y 'thumb_distal_position_y', 
  k.z 'thumb_distal_position_z', 

  l.x 'thumb_direction_x', 
  l.y 'thumb_direction_y', 
  l.z 'thumb_direction_z', 

  m.x 'index_tip_position_x', 
  m.y 'index_tip_position_y', 
  m.z 'index_tip_position_z', 

  n.x 'index_metacarpal_position_x', 
  n.y 'index_metacarpal_position_y', 
  n.z 'index_metacarpal_position_z', 

  o.x 'index_proximal_position_x', 
  o.y 'index_proximal_position_y', 
  o.z 'index_proximal_position_z', 

  p.x 'index_intermediate_position_x', 
  p.y 'index_intermediate_position_y', 
  p.z 'index_intermediate_position_z', 

  q.x 'index_distal_position_x', 
  q.y 'index_distal_position_y', 
  q.z 'index_distal_position_z', 

  r.x 'index_direction_x', 
  r.y 'index_direction_y', 
  r.z 'index_direction_z', 

  s.x 'middle_tip_position_x', 
  s.y 'middle_tip_position_y', 
  s.z 'middle_tip_position_z', 

  t.x 'middle_metacarpal_position_x', 
  t.y 'middle_metacarpal_position_y', 
  t.z 'middle_metacarpal_position_z', 

  u.x 'middle_proximal_position_x', 
  u.y 'middle_proximal_position_y', 
  u.z 'middle_proximal_position_z', 

  v.x 'middle_intermediate_position_x', 
  v.y 'middle_intermediate_position_y', 
  v.z 'middle_intermediate_position_z', 

  w.x 'middle_distal_position_x', 
  w.y 'middle_distal_position_y', 
  w.z 'middle_distal_position_z', 

  x.x 'middle_direction_x', 
  x.y 'middle_direction_y', 
  x.z 'middle_direction_z', 

  y.x 'ring_tip_position_x', 
  y.y 'ring_tip_position_y', 
  y.z 'ring_tip_position_z', 

  z.x 'ring_metacarpal_position_x', 
  z.y 'ring_metacarpal_position_y', 
  z.z 'ring_metacarpal_position_z', 

  aa.x 'ring_proximal_position_x', 
  aa.y 'ring_proximal_position_y', 
  aa.z 'ring_proximal_position_z', 

  ab.x 'ring_intermediate_position_x', 
  ab.y 'ring_intermediate_position_y', 
  ab.z 'ring_intermediate_position_z', 
  
  ac.x 'ring_distal_position_x', 
  ac.y 'ring_distal_position_y', 
  ac.z 'ring_distal_position_z', 
  
  ad.x 'ring_direction_x', 
  ad.y 'ring_direction_y', 
  ad.z 'ring_direction_z', 

  ae.x 'pinky_tip_position_x', 
  ae.y 'pinky_tip_position_y', 
  ae.z 'pinky_tip_position_z', 

  af.x 'pinky_metacarpal_position_x', 
  af.y 'pinky_metacarpal_position_y', 
  af.z 'pinky_metacarpal_position_z', 

  ag.x 'pinky_proximal_position_x', 
  ag.y 'pinky_proximal_position_y', 
  ag.z 'pinky_proximal_position_z', 

  ah.x 'pinky_intermediate_position_x', 
  ah.y 'pinky_intermediate_position_y', 
  ah.z 'pinky_intermediate_position_z', 

  ai.x 'pinky_distal_position_x', 
  ai.y 'pinky_distal_position_y', 
  ai.z 'pinky_distal_position_z', 

  aj.x 'pinky_direction_x', 
  aj.y 'pinky_direction_y', 
  aj.z 'pinky_direction_z' 

  FROM handData a  

  LEFT JOIN Coordinate b ON a.palm_position=b.id 
  LEFT JOIN Coordinate c ON a.palm_direction=c.id 
  LEFT JOIN Coordinate d ON a.palm_normal_direction=d.id 
  LEFT JOIN Coordinate e ON a.wrist_position=e.id 
  LEFT JOIN Coordinate f ON a.hand_sphere_radius=f.id

  LEFT JOIN Coordinate g ON a.thumb_tip_position=g.id 
  LEFT JOIN Coordinate h ON a.thumb_metacarpal_position=h.id 
  LEFT JOIN Coordinate i ON a.thumb_proximal_position=i.id 
  LEFT JOIN Coordinate j ON a.thumb_intermediate_position=j.id 
  LEFT JOIN Coordinate k ON a.thumb_distal_position=k.id 
  LEFT JOIN Coordinate l ON a.thumb_direction=l.id 

  LEFT JOIN Coordinate m ON a.index_tip_position=m.id 
  LEFT JOIN Coordinate n ON a.index_metacarpal_position=n.id 
  LEFT JOIN Coordinate o ON a.index_proximal_position=o.id 
  LEFT JOIN Coordinate p ON a.index_intermediate_position=p.id 
  LEFT JOIN Coordinate q ON a.index_distal_position=q.id 
  LEFT JOIN Coordinate r ON a.index_direction=r.id 

  LEFT JOIN Coordinate s ON a.middle_tip_position=s.id 
  LEFT JOIN Coordinate t ON a.middle_metacarpal_position=t.id 
  LEFT JOIN Coordinate u ON a.middle_proximal_position=u.id 
  LEFT JOIN Coordinate v ON a.middle_intermediate_position=v.id 
  LEFT JOIN Coordinate w ON a.middle_distal_position=w.id 
  LEFT JOIN Coordinate x ON a.middle_direction=x.id 

  LEFT JOIN Coordinate y ON a.ring_tip_position=y.id 
  LEFT JOIN Coordinate z ON a.ring_metacarpal_position=z.id 
  LEFT JOIN Coordinate aa ON a.ring_proximal_position=aa.id 
  LEFT JOIN Coordinate ab ON a.ring_intermediate_position=ab.id 
  LEFT JOIN Coordinate ac ON a.ring_distal_position=ac.id 
  LEFT JOIN Coordinate ad ON a.ring_direction=ad.id 

  LEFT JOIN Coordinate ae ON a.pinky_tip_position=ae.id 
  LEFT JOIN Coordinate af ON a.pinky_metacarpal_position=af.id 
  LEFT JOIN Coordinate ag ON a.pinky_proximal_position=ag.id 
  LEFT JOIN Coordinate ah ON a.pinky_intermediate_position=ah.id 
  LEFT JOIN Coordinate ai ON a.pinky_distal_position=ai.id 
  LEFT JOIN Coordinate aj ON a.pinky_direction=aj.id