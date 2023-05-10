from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import randint
window.title='太空危机 By:3084793958'
key_help=Entity()
player_help=Entity()
dr_help=Entity()
dr_tiger_help=Entity()
plane_time=Entity(x=3)
f1_find=Entity(choose=False)
t34_find=Entity(choose=False)
ju87_zd_find=Entity(choose=False)
tiger_find=Entity(choose=False)
class life_bag(Entity):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.model='files/3d/food/help.obj'
        self.scale=0.2
        self.color=color.white
        self.collider='box'
    def update(self):
        if distance(self,player)<3:
            if player.hp<=490:
                player.hp+=10
            else:
                if not player.god:
                    player.hp=500
            show_ppsh41.sl+=71
            show_ptrd41.sl+=2
            show_f1.sl+=1
            if player.plane_zd<=250:
                player.plane_zd+=50
            else:
                if not player.god:
                    player.plane_zd=300
            if t34.life<=4500:
                t34.life+=500
            else:
                if not player.god:
                    t34.life=5000
            destroy(self)
class dr_zd(Entity):
    def __init__(self,speed=1000,lifetime=7,**kwargs):
        super().__init__(**kwargs)
        self.model='files/3d/ppsh41/ppsh41zd.obj'
        self.scale=0.05
        self.collider='box'
        self.speed = speed
        self.lifetime = lifetime
        self.color=color.orange
        self.start = time.time()
    def update(self):
        self.world_position += self.forward * self.speed * time.dt
        if distance(self,player)<3 and player.on_t34==False:
            player.hp-=1
            destroy(self,delay=0.1)
        if self.intersects().hit and not self.intersects(traverse_target=dr_help).hit:
            destroy(self)
        if time.time() - self.start >= self.lifetime:
            destroy(self)
class dr_zd2(Entity):
    def __init__(self,speed=1000,lifetime=7,**kwargs):
        super().__init__(**kwargs)
        self.model='files/3d/ppsh41/ppsh41zd.obj'
        self.scale=0.05
        self.collider='box'
        self.speed = speed
        self.lifetime = lifetime
        self.color=color.orange
        self.start = time.time()
    def update(self):
        self.world_position += self.forward * self.speed * time.dt
        if distance(self,player)<3 and player.on_t34==False:
            player.hp-=1
            destroy(self,delay=0.1)
        if self.intersects().hit and not self.intersects(traverse_target=dr_tiger_help).hit:
            destroy(self)
        if time.time() - self.start >= self.lifetime:
            destroy(self)
class dr_pd(Entity):
    def __init__(self,speed=500,lifetime=10,**kwargs):
        super().__init__(**kwargs)
        self.model='files/3d/ptrd41/ptrd41zd.obj'
        self.scale=0.05
        self.collider='box'
        self.speed = speed
        self.lifetime = lifetime
        self.color=color.orange
        self.start = time.time()
    def update(self):
        self.world_position += self.forward * self.speed * time.dt
        if (self.intersects().hit and not self.intersects(traverse_target=dr_tiger_help).hit) or distance(self,player)<5:
            ju87_zd_find.choose=True
            invoke(Audio, 'files/sound/boom.ogg')
            boom = Entity(model = 'cube',texture = 'files/image/boom.png',position = self.world_position,scale=1.5)
            ju87_zd_find.position=boom.world_position
            destroy(boom,delay = 5)
            invoke(setattr, ju87_zd_find, 'choose', False, delay=0.1)
            destroy(self)
        if time.time() - self.start >= self.lifetime:
            destroy(self)
class F1_main(Entity):
    def __init__(self,speed=1000,lifetime=7,**kwargs):
        super().__init__(**kwargs)
        self.model='files/3d/f1/f1a.obj'
        self.scale=0.02
        self.collider='box'
        self.speed = speed
        self.lifetime = lifetime
        self.start = time.time()
        self.world_rotation_x-=0.03
    def update(self):
        self.world_position += self.forward * self.speed * time.dt
        if self.world_rotation_x < 90:
                self.world_rotation_x+=0.3
        self.speed-=0.1
        if self.intersects().hit:
            self.rotation=-self.rotation
            self.world_position += self.forward * self.speed * time.dt
        if time.time() - self.start >= self.lifetime:
            f1_find.choose=True
            self.world_position += self.forward * self.speed * time.dt
            invoke(Audio, 'files/sound/boom.ogg')
            boom = Entity(model = 'cube',texture = 'files/image/boom.png',position = self.world_position,scale=1)
            f1_find.position=boom.world_position
            destroy(self)
            destroy(boom,delay = 5)
            invoke(setattr, f1_find, 'choose', False, delay=0.1)
class F1_main_right(Entity):
    def __init__(self,speed=1000,lifetime=7,**kwargs):
        super().__init__(**kwargs)
        self.model='files/3d/f1/f1a.obj'
        self.scale=0.02
        self.collider='box'
        self.speed = speed
        self.lifetime = lifetime
        self.start = time.time()
        self.world_rotation_x-=0.03
    def update(self):
        self.world_position += self.forward * self.speed * time.dt
        if self.world_rotation_x < 90:
                self.world_rotation_x+=0.3
        self.speed-=0.1
        if time.time() - self.start >= self.lifetime or self.intersects().hit:
            f1_find.choose=True
            self.world_position += self.forward * self.speed * time.dt
            invoke(Audio, 'files/sound/boom.ogg')
            boom = Entity(model = 'cube',texture = 'files/image/boom.png',position = self.world_position,scale=1)
            f1_find.position=boom.world_position
            destroy(self)
            destroy(boom,delay = 5)
            invoke(setattr, f1_find, 'choose', False, delay=0.1)
class dl_a(Entity):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.parent=dr_help
        self.model='files/3d/dr/simple/a.obj'
        self.collider='box'
        self.color=color.white
        self.dr_hp=100
        self.on_cooldown=False
        self.dying=False
        self.start_killing=False
        self.number_now=30
        self.zd_cool=False
    def update(self):
        if mouse.hovered_entity==self and player.wq==1 and held_keys['left mouse'] and show_ppsh41.now_sl!=0:
            self.dr_hp-=10
            if self.dr_hp>0:
                self.look_at(player)
                self.rotation_y+=90
                self.start_killing=True
        if mouse.hovered_entity==self and player.wq==4 and held_keys['left mouse'] and player.plane_zd!=0:
            self.dr_hp-=20
            if self.dr_hp>0:
                self.look_at(camera)
                self.rotation_y+=90
                self.start_killing=True
        if mouse.hovered_entity==self and player.wq==2 and ptrd41_zd.enabled==True:
            self.dr_hp-=2000
        if f1_find.choose==True and distance(self,f1_find)<15:
            self.dr_hp-=(15-int(distance(self,f1_find)))*10
        if ju87_zd_find.choose==True and distance(self,ju87_zd_find)<20:
            self.dr_hp-=(20-int(distance(self,ju87_zd_find)))*10
        if tiger_find.choose==True and distance(self,tiger_find)<20:
            self.dr_hp-=(20-int(distance(self,tiger_find)))*60
        if key_help.z==1 and player.wq==4:
            if distance(self,auto_plane_main)<3:
                if distance(t34,auto_plane_main)<10:
                    t34.life-=30*(15-int(distance(t34,auto_plane_main)))
                key_help.z=0
                camera.position=(0,0,0)
                camera.rotation=(0,0,0)
                player.speed=5
                player.jump_height=9
                zg_main.parent=player
                auto_plane_ctrl.parent=player
                auto_plane_ctrl.enabled=False
                auto_plane_main.enabled=False
                camera.parent=player.camera_pivot
                plane_show_distance.enabled=False
                plane_show_pos.enabled=False
                plane_show_player_rotation.enabled=False
                plane_show_player_pos.enabled=False
                plane_show_zd.enabled=False
                ppsh41.enabled=True
                ptrd41.enabled=False
                f1.enabled=False
                show_plane_ctrl.color=color.white50
                player.wq=1
                plane_time.x-=1
                player.plane_audio.stop()
                if pow((player.x-auto_plane_main.x)**2+(player.z-auto_plane_main.z)**2,0.5)<3 and abs(player.y-auto_plane_main.y+0.25)<3:
                    player.hp-=80
                    be_hurt()
                invoke(Audio, 'plane_boom.ogg')
                self.dr_hp-=80
        if t34_find.choose==True and distance(self,t34_find)<15:
            self.dr_hp-=(15-int(distance(self,t34_find)))*100
        if mouse.hovered_entity==self and player.wq==6 and held_keys['left mouse'] and show_t34_zd.sl!=0:
            self.dr_hp-=20
        if t34.speed!=0:
            if distance(self,t34)<10:
                self.dr_hp-=abs(int(t34.speed))*50
                if self.dr_hp>0:
                    self.look_at(player)
                    self.rotation_y+=90
                    self.start_killing=True
        if (self.start_killing or distance(self,player)<30)and not self.dying:
            self.look_at(zg_main)
            self.rotation_y+=90
            if self.on_cooldown==False and self.zd_cool==False:
                self.zd_cool=True
                invoke(setattr, self, 'zd_cool', False, delay=0.1)
                self.number_now-=1
                invoke(Audio, 'jq.wav')
                dr_zd(world_rotation=self.world_rotation-(0,90,0),world_position=self.world_position)
                if self.number_now<=0:
                    self.on_cooldown=True
                    if random.randint(1,2)==1:
                        F1_main_right(world_position=self.world_position+(0,3,0),world_rotation=self.world_rotation-(0,90,0)-(((pow((self.x-player.x)**2+(self.z-player.z)**2,0.5)/2)/36)*0.3)+10)
                    invoke(setattr, self, 'on_cooldown', False, delay=10)
                    invoke(setattr, self, 'number_now', 30, delay=9)
        if self.dr_hp<=0 and self.dying==False:
            self.dying=True
            player.kill+=1
            self.rotation_z=90
            life_bag(world_position=self.world_position)
            destroy(self,delay=2)
class tiger(Entity):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.parent=dr_tiger_help
        self.model='files/3d/dr/tiger/tigerd.obj'
        self.pt=Entity(model='tigerpt.obj',collider='box',color=color.black,parent=self,position=(0,4.5,0))
        self.p=Entity(model='tigerp.obj',collider='box',color=color.white, parent=self.pt, position=(-0.5,1.4,0))
        self.collider='box'
        self.color=color.light_gray
        self.dr_hp=7000
        self.dying=False
        self.fdj_audio=Audio('files/sound/fdj.ogg',loop=True,auto_destroy=False)
        self.on_cooldown=False
        self.dying=False
        self.number_now=50
        self.zd_cool=False
        self.p_help=Entity(parent=self.pt)
    def update(self):
        self.pt.look_at(zg_main, axis='left')
        self.pt.rotation_x=0
        self.pt.rotation_z=0
        self.p.look_at(zg_main, axis='left')
        if self.p.rotation_z>25:
            self.p.rotation_z=25
        if self.p.rotation_z<-5:
            self.p.rotation_z=-5
        self.p_help.look_at(zg_main)
        if (mouse.hovered_entity==self or mouse.hovered_entity==self.p or mouse.hovered_entity==self.pt) and player.wq==2 and ptrd41_zd.enabled==True:
            self.dr_hp-=2000
        if f1_find.choose==True and distance(self,f1_find)<15:
            self.dr_hp-=(15-int(distance(self,f1_find)))*10
        if ju87_zd_find.choose==True and distance(self,ju87_zd_find)<20:
            self.dr_hp-=(20-int(distance(self,ju87_zd_find)))*30
        if tiger_find.choose==True and distance(self,tiger_find)<20:
            self.dr_hp-=(20-int(distance(self,tiger_find)))*60
        if key_help.z==1 and player.wq==4:
            if distance(self,auto_plane_main)<15:
                if distance(t34,auto_plane_main)<15:
                    t34.life-=30*(15-int(distance(t34,auto_plane_main)))
                key_help.z=0
                camera.position=(0,0,0)
                camera.rotation=(0,0,0)
                player.speed=5
                player.jump_height=9
                zg_main.parent=player
                auto_plane_ctrl.parent=player
                auto_plane_ctrl.enabled=False
                auto_plane_main.enabled=False
                camera.parent=player.camera_pivot
                plane_show_distance.enabled=False
                plane_show_pos.enabled=False
                plane_show_player_rotation.enabled=False
                plane_show_player_pos.enabled=False
                plane_show_zd.enabled=False
                ppsh41.enabled=True
                ptrd41.enabled=False
                f1.enabled=False
                show_plane_ctrl.color=color.white50
                player.wq=1
                plane_time.x-=1
                player.plane_audio.stop()
                if pow((player.x-auto_plane_main.x)**2+(player.z-auto_plane_main.z)**2,0.5)<3 and abs(player.y-auto_plane_main.y+0.25)<3:
                    player.hp-=80
                    be_hurt()
                invoke(Audio, 'plane_boom.ogg')
                self.dr_hp-=80
        if t34_find.choose==True and distance(self,t34_find)<15:
            self.dr_hp-=(15-int(distance(self,t34_find)))*random.randint(50,400)
        if t34.speed!=0:
            if distance(self,t34)<15:
                if abs(t34.speed)>1:
                    self.dr_hp-=abs(int(t34.speed))*50
                t34.speed=0
        if self.dying==False:
            if distance(player,self)>70:
                if self.fdj_audio.playing==True:
                    self.fdj_audio.stop()
            else:
                if self.fdj_audio.playing==False:
                    self.fdj_audio.play()
        if self.dr_hp<=0 and self.dying==False:
            self.dying=True
            player.kill+=1
            self.fdj_audio.stop()
            destroy(self,delay=2)
        if distance(self,player)<100:
            if self.on_cooldown==False and self.zd_cool==False:
                self.zd_cool=True
                invoke(setattr, self, 'zd_cool', False, delay=0.1)
                self.number_now-=1
                invoke(Audio, 'jq.wav')
                dr_zd2(world_rotation=(self.p_help.world_rotation_x+1.25,self.p.world_rotation_y-90,self.p_help.world_rotation_z),world_position=self.p.world_position)
                if self.number_now<=0:
                    self.on_cooldown=True
                    invoke(setattr, self, 'on_cooldown', False, delay=10)
                    invoke(setattr, self, 'number_now', 50, delay=9)
                    invoke(Audio, 'ptrd41.ogg')
                    dr_pd(world_rotation=(self.p_help.world_rotation_x+1.25,self.p_help.world_rotation_y,self.p_help.world_rotation_z),world_position=self.p.world_position)
class ju_87(Entity):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.parent=dr_help
        self.model='files/3d/dr/ju87/ju87ga.obj'
        self.lxj=Entity(model='files/3d/dr/ju87/ju87gb.obj',color=color.white,parent=self,position=(0,0,11))
        self.zd=Entity(model='files/3d/dr/ju87/ju87gc.obj',color=color.gray,parent=self,position=(0,-2.2,4.5),collider='box')
        self.collider='box'
        self.color=color.green
        self.dr_hp=500
        self.dying=False
        self.turn_on_cooldown=False
        self.speed=11
        self.throwing=False
        self.zd_died=False
        self.plane_audio=Audio('files/sound/fj.ogg',loop=True,auto_destroy=False)
    def update(self):
        if distance_xz(self,player)<self.y*11/10 and distance_xz(self,player)>self.y and self.throwing==False:
            self.throwing=True
        if self.zd_died==True:
            invoke(setattr, self, 'zd_died', False, delay=10)
        if self.zd_died==True and self.throwing==True:
            self.zd.y=-2.2
            self.throwing=False
        if self.throwing==True and self.zd_died==False:
            self.zd.y-=1
            if self.zd.world_y<-25:
                self.zd_died=True
            if self.zd.intersects(ignore=(self,)).hit:
                boom = Entity(model = 'cube',texture = 'files/image/boom.png',position = self.zd.world_position,scale=1.5)
                self.zd_died=True
                ju87_zd_find.choose=True
                invoke(Audio, 'files/sound/boom.ogg')
                ju87_zd_find.position=boom.world_position
                destroy(boom,delay = 5)
                invoke(setattr, ju87_zd_find, 'choose', False, delay=0.1)
        if self.turn_on_cooldown==False and not self.throwing:
            self.turn_on_cooldown=True
            invoke(setattr, self, 'turn_on_cooldown', False, delay=15)
            self.look_at(player)
        self.rotation_x=0
        self.rotation_z=0
        if self.speed>0:
            self.position+=self.forward*self.speed/10
        else:
            self.y-=0.5
            self.position+=self.forward
        self.lxj.rotation_z+=10
        if mouse.hovered_entity==self and player.wq==1 and held_keys['left mouse'] and show_ppsh41.now_sl!=0:
            self.dr_hp-=5
        if mouse.hovered_entity==self and player.wq==4 and held_keys['left mouse'] and player.plane_zd!=0:
            self.dr_hp-=7
        if mouse.hovered_entity==self and player.wq==2 and ptrd41_zd.enabled==True:
            self.dr_hp-=2000
        if f1_find.choose==True and distance(self,f1_find)<30:
            self.dr_hp-=(30-int(distance(self,f1_find)))*10
        if key_help.z==1 and player.wq==4:
            if distance(self,auto_plane_main)<30:
                if distance(t34,auto_plane_main)<15:
                    t34.life-=30*(15-int(distance(t34,auto_plane_main)))
                key_help.z=0
                camera.position=(0,0,0)
                camera.rotation=(0,0,0)
                player.speed=5
                player.jump_height=9
                zg_main.parent=player
                auto_plane_ctrl.parent=player
                auto_plane_ctrl.enabled=False
                auto_plane_main.enabled=False
                camera.parent=player.camera_pivot
                plane_show_distance.enabled=False
                plane_show_pos.enabled=False
                plane_show_player_rotation.enabled=False
                plane_show_player_pos.enabled=False
                plane_show_zd.enabled=False
                ppsh41.enabled=True
                ptrd41.enabled=False
                f1.enabled=False
                show_plane_ctrl.color=color.white50
                player.wq=1
                plane_time.x-=1
                player.plane_audio.stop()
                if pow((player.x-auto_plane_main.x)**2+(player.z-auto_plane_main.z)**2,0.5)<3 and abs(player.y-auto_plane_main.y+0.25)<3:
                    player.hp-=80
                    be_hurt()
                invoke(Audio, 'plane_boom.ogg')
                self.dr_hp-=80
        if t34_find.choose==True and distance(self,t34_find)<30:
            self.dr_hp-=(30-int(distance(self,t34_find)))*random.randint(50,400)
        if ju87_zd_find.choose==True and distance(self,ju87_zd_find)<20:
            self.dr_hp-=(20-int(distance(self,ju87_zd_find)))*10
        if tiger_find.choose==True and distance(self,tiger_find)<20:
            self.dr_hp-=(20-int(distance(self,tiger_find)))*60
        if mouse.hovered_entity==self and player.wq==6 and held_keys['left mouse'] and show_t34_zd.sl!=0:
            self.dr_hp-=10
        if self.dying==False:
            if distance(player,self)>200:
                if self.plane_audio.playing==True:
                    self.plane_audio.stop()
            else:
                if self.plane_audio.playing==False:
                    self.plane_audio.play()
        if self.dr_hp<=0 and self.dying==False:
            self.dying=True
            player.kill+=1
            self.plane_audio.stop()
            destroy(self,delay=3)
            invoke(Audio, 'files/sound/boom.ogg',delay=3)
def key_input(key):
    if key=='escape':
        quit()
    if key=='c':
        print(player.kill,player.hp)
    if key=='space':
        if jump_time.x<1 and player.air_time!=0:
            player.air_time=0
            player.will_hp=0
            player.grounded=True
            player.jump()
            jump_time.x+=1
    if (key=='enter'or key=='4') and player.air_time==0 and plane_time.x>0 and key_help.z!=2 and player.on_r==False and key_help.z!=2 and player.on_r==False and player.on_eat==False and not player.on_t34:
        if key_help.z==0:
            auto_plane_main.position=player.position+(0,3,0)
            key_help.z=1
            auto_plane_ctrl.enabled=True
            auto_plane_main.enabled=True
            player.speed=0
            player.jump_height=0
            player_help.position=player.position
            player_help.rotation=player.rotation
            zg_main.parent=player_help
            auto_plane_ctrl.parent=player_help
            camera.parent=scene
            plane_show_distance.enabled=True
            plane_show_pos.enabled=True
            plane_show_player_rotation.enabled=True
            plane_show_player_pos.enabled=True
            plane_show_zd.enabled=True
            ppsh41.enabled=False
            ptrd41.enabled=False
            f1.enabled=False
            player.plane_audio.play()
            show_plane_ctrl.color=color.white
            show_ppsh41.color=color.white50
            show_ptrd41.color=color.white50
            show_f1.color=color.white50
            player.wq=4
        else:
            key_help.z=0
            camera.position=(0,0,0)
            camera.rotation=(0,0,0)
            player.speed=5
            player.jump_height=9
            zg_main.parent=player
            auto_plane_ctrl.parent=player
            auto_plane_ctrl.enabled=False
            auto_plane_main.enabled=False
            camera.parent=player.camera_pivot
            plane_show_distance.enabled=False
            plane_show_pos.enabled=False
            plane_show_player_rotation.enabled=False
            plane_show_player_pos.enabled=False
            plane_show_zd.enabled=False
            ppsh41.enabled=True
            ptrd41.enabled=False
            f1.enabled=False
            player.plane_audio.stop()
            show_plane_ctrl.color=color.white50
            show_ppsh41.color=color.white
            show_ptrd41.color=color.white50
            show_f1.color=color.white50
            player.wq=1
    if key=='1' and player.on_r==False and key_help.z!=2 and player.on_eat==False and not player.on_t34:
        wq_1()
    if key=='2' and player.on_r==False and key_help.z!=2 and player.on_eat==False and not player.on_t34:
        wq_2()
    if key=='3' and player.on_r==False and key_help.z!=2 and player.on_eat==False and not player.on_t34:
        wq_3()
    if key=='scroll down' and player.on_r==False and key_help.z!=2 and player.on_eat==False and not player.on_t34:
        if player.wq!=4:
            player.wq+=1
            if player.wq==3:
                wq_3()
            if player.wq==2:
                wq_2()
            if player.wq==4:
                wq_4()
        else:
            player.wq=1
            wq_1()
    if key=='scroll up' and player.on_r==False and key_help.z!=2 and player.on_eat==False and not player.on_t34:
        if player.wq!=1:
            player.wq-=1
            if player.wq==3:
                wq_3()
            if player.wq==2:
                wq_2()
            if player.wq==1:
                wq_1()
        else:
            player.wq=4
            wq_4()
    if key=='right mouse down' and player.wq!=4 and jump_time.y==0 and player.on_r==False and key_help.z==0 and player.on_eat==False and not player.on_t34:
        player.left_ing=not player.left_ing
        if ppsh41.rotation_y == 87:
            ppsh41.position = (0, -0.087, 0.45)
            ppsh41.rotation_y = 90
        else:
            ppsh41.position = (0.15, -0.1, 0.35)
            ppsh41.rotation_y = 87
        if ptrd41.rotation_y == 87:
            ptrd41.position = (0, -0.29, 0.4)
            ptrd41.rotation_y = 90
        else:
            ptrd41.position = (0.15, -0.3, 0.9)
            ptrd41.rotation_y = 87
        if f1.rotation_z == 0:
            f1.rotation_z = 90
        else:
            f1.rotation_z = 0
    if key=='r' and player.on_r==False and key_help.z==0 and player.on_eat==False and not player.on_t34:
        if player.wq==1 and show_ppsh41.now_sl!=71 and show_ppsh41.sl>0:
            player.on_r=True
            for x in range(36):
                ppsh41.animate_rotation_y(5, duration=0.5)
                ppsh41.animate_rotation_z(15, duration=0.5)
                ppsh41.animate_rotation_x(15, duration=0.5)
            invoke(Audio, 'r1.ogg', delay=0.7)
            ppsh41dj.animate_y(-25, duration=0.7, delay=0.5)
            ppsh41dj.animate_y(-2, duration=0.7, delay=1.2)
            invoke(Audio, 'r1.ogg', delay=1.9)
            if ppsh41.position == (0.15, -0.1, 0.35):
                ppsh41.animate_rotation_y(87, duration=0.5, delay=1.9)
            if ppsh41.position == (0, -0.087, 0.45):
                ppsh41.animate_rotation_y(90, duration=0.5, delay=1.9)
            ppsh41.animate_rotation_z(0, duration=0.5, delay=1.9)
            ppsh41.animate_rotation_x(0, duration=0.5, delay=1.9)
            invoke(setattr, player, 'on_r', False, delay=2)
        if player.wq==2 and show_ptrd41.now_sl==0 and show_ptrd41.sl!=0 and player.on_eat==False  and not player.on_t34:
            player.on_r=True
            for x in range(36):
                ptrd41.animate_rotation_y(5, duration=1)
                ptrd41.animate_rotation_z(15, duration=1)
                ptrd41.animate_rotation_x(15, duration=1)
            invoke(Audio, 'r2.ogg', delay=1)
            ptrd41d.animate_y(-50, duration=1, delay=0.9)
            ptrd41d.animate_y(30, duration=0.001, delay=2)
            ptrd41d.animate_y(4.7, duration=1, delay=2.1)
            invoke(Audio, 'r2.ogg', delay=3.1)
            if ptrd41.position == (0.15, -0.3, 0.9):
                ptrd41.animate_rotation_y(87, duration=1.5, delay=3.5)
            if ptrd41.position == (0, -0.29, 0.4):
                ptrd41.animate_rotation_y(90, duration=1.5, delay=3.5)
            ptrd41.animate_rotation_z(0, duration=0.5, delay=7.6)
            ptrd41.animate_rotation_x(0, duration=0.5, delay=7.6)
            invoke(setattr, player, 'on_r', False, delay=7.9)
    if key=='left mouse down' and player.on_r==False and key_help.z==0 and player.on_eat==False and not player.on_t34:
        if player.wq==2 and show_ptrd41.now_sl!=0:
            ptrd41_zd.enabled=True
            invoke(setattr,ptrd41_zd,'enabled',False, delay=.03)
            show_ptrd41.now_sl-=1
            invoke(Audio, 'ptrd41.ogg')
            if not player.left_ing:
                player.hp-=30
                be_hurt()
            if mouse.hovered_entity and hasattr(mouse.hovered_entity,'hp_t34') and not player.god:
                t34.life-=2000
                t34_be_hurt()
            if not player.left_ing:
                mouse.position=random.randint(-1,1)/12,random.randint(-1,1)/6
            else:
                mouse.position=random.randint(-1,1)/30,random.randint(-1,1)/18
        if player.wq==3 and show_f1.sl!=0 and show_f1.on_cooldown==False:
            show_f1.on_cooldown=True
            invoke(setattr, show_f1, 'on_cooldown', False, delay=4)
            if not player.left_ing:
                F1_main(world_position=player.camera_pivot.world_position,world_rotation=player.camera_pivot.world_rotation)
            else:
                F1_main_right(world_position=player.camera_pivot.world_position,world_rotation=player.camera_pivot.world_rotation)
            show_f1.sl-=1
    if key=='left mouse down' and player.on_t34:
        if player.wq==5 and show_t34_cjd.sl!=0:
            invoke(Audio, 'ptrd41.ogg')
            show_t34_cjd.sl-=1
            p_fire()
            if mouse.hovered_entity:
                boom = Entity(model = 'cube',texture = 'files/image/boom.png',position = mouse.world_point,scale=1)
                invoke(Audio, 'boom.ogg',delay=0.3)
                t34_find.position=boom.world_position
                t34_find.choose=True
                invoke(setattr, t34_find, 'choose', False, delay=0.1)
                destroy(boom,delay = 5)
    if key=='r' and player.on_t34:
        if player.wq==5 and show_t34_cjd.sl==0 and not show_t34_cjd.on_cooldown:
            invoke(Audio, 'r2.ogg', delay=1)
            invoke(Audio, 'r2.ogg', delay=8)
            invoke(setattr, show_t34_cjd, 'on_cooldown', False, delay=10)
            invoke(setattr, show_t34_cjd, 'sl', show_t34_cjd.sl+1, delay=10)
        if player.wq==6 and show_t34_zd.sl==0 and not show_t34_zd.on_cooldown:
            invoke(Audio, 'r1.ogg', delay=1)
            invoke(Audio, 'r1.ogg', delay=5)
            invoke(setattr, show_t34_zd, 'on_cooldown', False, delay=8)
            invoke(setattr, show_t34_zd, 'sl', 50, delay=8)
    if key=='h' and player.wq!=4 and player.on_eat==False and player.on_r==False and key_help.z==0 and player.sl_food>0 and not player.on_t34:
        player.on_eat=True
        player.sl_food-=1
        invoke(setattr, player, 'on_eat', False, delay=11)
        if player.wq==1:
            ppsh41.enabled=False
            invoke(setattr, ppsh41,'enabled', True, delay=11)
        if player.wq==2:
            ptrd41.enabled=False
            invoke(setattr, ptrd41,'enabled', True, delay=11)
        if player.wq==3:
            f1.enabled=False
            invoke(setattr, f1,'enabled', True, delay=11)
        tea.enabled=True
        food_long.enabled=True
        tea.animate_position((0,0,0),duration=2.5)
        invoke(Audio,'drink.ogg',delay=2.5)
        tea.animate_position((-0.2,0,0.15),duration=2.5,delay=2.5)
        food_long.animate_position((0,0,0),duration=2.5,delay=5)
        invoke(Audio,'eat.ogg',delay=7.5)
        food_long.animate_position((0.1,0,0.15),duration=2.5,delay=7.5)
        invoke(setattr, tea,'enabled', False, delay=11)
        invoke(setattr, food_long,'enabled', False, delay=11)
        if player.hp<=250:
            invoke(setattr, player, 'hp', player.hp+50, delay=11)
        if player.hp>250 and player.hp<300:
            invoke(setattr, player, 'hp', 300, delay=11)
    if key=='g':
        if player.god==False:
            player.to_god.stop()
            player.to_god.play()
            main_ground.color=color.white33
            main_ground2.color=color.white33
            main_ground3.color=color.white33
            t34.color=color.rgba(0,42,0,33)
            t34p.color=color.white33
            t34pt.color=color.white33
        else:
            main_ground.color=color.white
            main_ground2.color=color.white
            main_ground3.color=color.white
            t34.color=color.rgba(0,42,0)
            t34p.color=color.white
            t34pt.color=color.white
        player.god=not player.god
        t34.can_throw=player.god
    if key=='f'and distance(player,t34)<7 and player.air_time==0 and player.on_r==False and key_help.z==0 and player.on_eat==False and t34.life>0:
        player.on_t34=not player.on_t34
        if player.on_t34:
            player.t34_audio.play()
            ppsh41.enabled=False
            ptrd41.enabled=False
            f1.enabled=False
            show_ppsh41.enabled=False
            show_ptrd41.enabled=False
            show_f1.enabled=False
            show_plane_ctrl.enabled=False
            show_t34_cjd.enabled=True
            show_t34_zd.enabled=True
            show_t34_life.enabled=True
            show_t34_cjd.color=color.white
            show_t34_zd.color=color.white50
            player.jump_height=0
            player.speed=0
            player.wq=5
            player_t34_help.position=t34pt.world_position+(0,0.7,0)
            player.position=t34.position+(0,2, 0)+t34.forward*4
            t34pt.collider=None
            t34p.collider=None
        else:
            player.t34_audio.stop()
            ppsh41.enabled=True
            ptrd41.enabled=False
            f1.enabled=False
            show_ppsh41.enabled=True
            show_ptrd41.enabled=True
            show_f1.enabled=True
            show_plane_ctrl.enabled=True
            show_t34_cjd.enabled=False
            show_t34_zd.enabled=False
            show_t34_life.enabled=False
            show_plane_ctrl.color=color.white50
            show_ppsh41.color=color.white
            show_ptrd41.color=color.white50
            show_f1.color=color.white50
            player.wq=1
            player.jump_height=9
            player.speed=5
            t34pt.collider='t34pt.obj'
            t34p.collider='t34p.obj'
    if player.on_t34:
        if key=='1':
            wq_5()
        if key=='2':
            wq_6()
        if key=='scroll down' or key=='scroll up':
            if player.wq==5:
                wq_6()
            else:
                wq_5()
def wq_1():
    if key_help.z!=2:
        key_help.z=0
        player.speed=5
        player.jump_height=9
    camera.position=(0,0,0)
    camera.rotation=(0,0,0)
    zg_main.parent=player
    auto_plane_ctrl.parent=player
    auto_plane_ctrl.enabled=False
    auto_plane_main.enabled=False
    camera.parent=player.camera_pivot
    plane_show_distance.enabled=False
    plane_show_pos.enabled=False
    plane_show_player_rotation.enabled=False
    plane_show_player_pos.enabled=False
    plane_show_zd.enabled=False
    ppsh41.enabled=True
    ptrd41.enabled=False
    f1.enabled=False
    player.plane_audio.stop()
    show_plane_ctrl.color=color.white50
    show_ppsh41.color=color.white
    show_ptrd41.color=color.white50
    show_f1.color=color.white50
    player.wq=1
def wq_2():
    if key_help.z!=2:
        key_help.z=0
        player.speed=5
        player.jump_height=9
    camera.position=(0,0,0)
    camera.rotation=(0,0,0)
    zg_main.parent=player
    auto_plane_ctrl.parent=player
    auto_plane_ctrl.enabled=False
    auto_plane_main.enabled=False
    camera.parent=player.camera_pivot
    plane_show_distance.enabled=False
    plane_show_pos.enabled=False
    plane_show_player_rotation.enabled=False
    plane_show_player_pos.enabled=False
    plane_show_zd.enabled=False
    ppsh41.enabled=False
    ptrd41.enabled=True
    f1.enabled=False
    player.plane_audio.stop()
    show_plane_ctrl.color=color.white50
    show_ppsh41.color=color.white50
    show_ptrd41.color=color.white
    show_f1.color=color.white50
    player.wq=2
def wq_3():
    if key_help.z!=2:
        key_help.z=0
        player.speed=5
        player.jump_height=9
    camera.position=(0,0,0)
    camera.rotation=(0,0,0)
    zg_main.parent=player
    auto_plane_ctrl.parent=player
    auto_plane_ctrl.enabled=False
    auto_plane_main.enabled=False
    camera.parent=player.camera_pivot
    plane_show_distance.enabled=False
    plane_show_pos.enabled=False
    plane_show_player_rotation.enabled=False
    plane_show_player_pos.enabled=False
    plane_show_zd.enabled=False
    ppsh41.enabled=False
    ptrd41.enabled=False
    f1.enabled=True
    player.plane_audio.stop()
    show_plane_ctrl.color=color.white50
    show_ppsh41.color=color.white50
    show_ptrd41.color=color.white50
    show_f1.color=color.white
    player.wq=3
def wq_4():
    if player.air_time==0 and plane_time.x>0 and key_help.z==0:
        auto_plane_main.position=player.position+(0,3,0)
        key_help.z=1
        auto_plane_ctrl.enabled=True
        auto_plane_main.enabled=True
        player.speed=0
        player.jump_height=0
        player_help.position=player.position
        player_help.rotation=player.rotation
        zg_main.parent=player_help
        auto_plane_ctrl.parent=player_help
        camera.parent=scene
        plane_show_distance.enabled=True
        plane_show_pos.enabled=True
        plane_show_player_rotation.enabled=True
        plane_show_player_pos.enabled=True
        plane_show_zd.enabled=True
        ppsh41.enabled=False
        ptrd41.enabled=False
        f1.enabled=False
        player.plane_audio.play()
        show_plane_ctrl.color=color.white
        show_ppsh41.color=color.white50
        show_ptrd41.color=color.white50
        show_f1.color=color.white50
        player.wq=4
    else:
        if key_help.z!=2:
            key_help.z=0
            player.speed=5
            player.jump_height=9
        camera.position=(0,0,0)
        camera.rotation=(0,0,0)
        zg_main.parent=player
        auto_plane_ctrl.parent=player
        auto_plane_ctrl.enabled=False
        auto_plane_main.enabled=False
        camera.parent=player.camera_pivot
        plane_show_distance.enabled=False
        plane_show_pos.enabled=False
        plane_show_player_rotation.enabled=False
        plane_show_player_pos.enabled=False
        plane_show_zd.enabled=False
        ppsh41.enabled=True
        ptrd41.enabled=False
        f1.enabled=False
        player.plane_audio.stop()
        show_plane_ctrl.color=color.white50
        show_ppsh41.color=color.white
        show_ptrd41.color=color.white50
        show_f1.color=color.white50
        player.wq=1
def wq_5():
    show_t34_zd.color=color.white50
    show_t34_cjd.color=color.white
    player.wq=5
def wq_6():
    show_t34_zd.color=color.white
    show_t34_cjd.color=color.white50
    player.wq=6
def update():
    if player.x>-200:
        if random.randint(1,50)==1 and int(window.fps_counter.text)>40:
            for x in range(10):
                dl_a(position=(player.x+random.randint(-50,50),2,player.z+random.randint(-50,50)))
            tiger(position=(player.x+random.randint(-100,100),2,player.z+random.randint(-100,100)))
    if player.kill>=150 and not player.died and not player.win:
        player.win=True
        invoke(Audio, 'files/sound/winmusic.ogg')
    if player.hp<=0 and not player.god and player.died==False:
        player.died=True
        invoke(Audio, 'files/sound/no.ogg')
    if player.on_t34 and not player.god and t34.life<=0:
        player.t34_audio.stop()
        ppsh41.enabled=True
        ptrd41.enabled=False
        f1.enabled=False
        show_ppsh41.enabled=True
        show_ptrd41.enabled=True
        show_f1.enabled=True
        show_plane_ctrl.enabled=True
        show_t34_cjd.enabled=False
        show_t34_zd.enabled=False
        show_t34_life.enabled=False
        show_plane_ctrl.color=color.white50
        show_ppsh41.color=color.white
        show_ptrd41.color=color.white50
        show_f1.color=color.white50
        player.wq=1
        player.jump_height=9
        player.speed=5
        t34pt.collider='t34pt.obj'
        t34p.collider='t34p.obj'
    if player.on_t34:
        player_t34_help.position=t34pt.world_position+(0,0.7,0)
        player.position=t34pt.world_position+(0,0.7,0)
        t34pt.world_rotation=player.rotation+(0,90,0)
        if -12<-player.camera_pivot.world_rotation_x<20:
            t34p.world_rotation_z=-player.camera_pivot.world_rotation_x
        if held_keys['a']:
                t34.rotation_y-=0.7
        if held_keys['d']:
                t34.rotation_y+=0.7
        if held_keys['w']:
            if not player.god:
                if t34.speed<7:
                    t34.speed+=0.03
            else:
                t34.speed+=0.03
        if held_keys['s']:
            if not player.god:
                if t34.speed>-6:
                    t34.speed-=0.03
            else:
                t34.speed-=0.03
        t34.position+=(t34.forward/10)*t34.speed
        if player.camera_pivot.rotation_z>=0:
            player.camera_pivot.rotation_z=random.randint(-10,0)/50
        else:
            player.camera_pivot.rotation_z=random.randint(0,10)/50
            player.camera_pivot.y=1+random.randint(0,10)/1000
    else:
        if t34.speed>0:
            t34.speed-=0.1
        if t34.speed<0:
            t34.speed+=0.1
        if int(t34.speed*10)==0:
            t34.speed=0
        if t34.speed!=0:
            t34.position+=(t34.forward/10)*t34.speed
    if t34.speed!=0 and not player.god:
        if raycast(origin=t34.world_position-(0,2,0),direction=t34.forward,distance=10,traverse_target=stop_t34).hit or raycast(origin=t34.world_position-(0,2,0),direction=t34.back,distance=10,traverse_target=stop_t34).hit:
            if t34.speed>0.7:
                t34.life-=abs(int(t34.speed*100))
                invoke(Audio, 'plane_boom.ogg')
                t34_be_hurt()
            t34.position-=(t34.forward/10)*t34.speed
            t34.speed=0
    if player.god:
        player.hp=999
        show_ppsh41.sl=999
        show_ppsh41.now_sl=999
        show_ptrd41.sl=999
        show_ptrd41.now_sl=999
        show_f1.sl=999
        show_f1.now_sl=999
        plane_time.x=999
        player.will_hp=0
        player.plane_zd=999
        show_t34_cjd.sl=999
        show_t34_zd.sl=999
        t34.life=9999
        show_t34_cjd.on_cooldown=False
        show_t34_zd.on_cooldown=False
        show_f1.on_cooldown=False
        show_ptrd41.on_cooldown=False
        player.cursor.enabled=True
        hurt_show.enabled=False
        jump_time.x=0
        if not key_help.z==1 and not player.on_t34:
            player.jump_height=9
            player.speed=10
            key_help.z=0
    else:
        player.cursor.enabled=False
        hurt_show.enabled=True
    if (held_keys['q']or held_keys['e']) and player.wq!=4 and jump_time.y==0 and player.on_r==False and key_help.z==0 and player.on_eat==False and not player.on_t34:
        if held_keys['q']:
            camera.rotation_z=-30
        if held_keys['e']:
            camera.rotation_z=30
    else:
        camera.rotation_z=0
    if key_help.z==0 and not player.on_t34:
        if player.air_time!=0:
            player.speed=10
        else:
            if jump_time.y==1:
                player.speed=7
            else:
                player.speed=5
    if player.grounded==True and jump_time.x>=1:
        jump_time.x=0
    if player.speed!=10 and key_help.z==0 and player.left_ing==False and player.on_r==False and not player.on_t34:
        if held_keys['shift']:
            jump_time.y=1
            player.speed=7
            ppsh41.rotation_y=20
            ppsh41.x=0
            ptrd41.rotation_y=10
            ptrd41.x=0
        else:
            jump_time.y=0
            if not player.on_t34:
                player.speed=5
            ppsh41.rotation_y=87
            ppsh41.x=0.15
            ptrd41.rotation_y=87
            ptrd41.x=0.15
    if player.on_r==False:
        if ppsh41.rotation_x!=0 and player.wq==1:
            if show_ppsh41.sl > 71 - show_ppsh41.now_sl:
                show_ppsh41.sl -= 71 - show_ppsh41.now_sl
                show_ppsh41.now_sl = 71
            else:
                show_ppsh41.now_sl += show_ppsh41.sl
                show_ppsh41.sl = 0
        if ptrd41.rotation_x!=0 and player.wq==2:
            if show_ptrd41.now_sl==0:
                show_ptrd41.now_sl+=1
                show_ptrd41.sl-=1
    if ju87_zd_find.choose==True and distance(player,ju87_zd_find)<20 and not player.on_t34:
        player.hp-=(20-int(distance(player,ju87_zd_find)))*5
        be_hurt()
    if ju87_zd_find.choose==True and distance(t34,ju87_zd_find)<20:
        t34.life-=(20-int(distance(t34,ju87_zd_find)))*40
        t34_be_hurt()
    if ju87_zd_find.choose==True and distance(ju87_zd_find,auto_plane_main)<20 and key_help.z==1:
        key_help.z=0
        camera.position=(0,0,0)
        camera.rotation=(0,0,0)
        if not player.on_t34:
            player.speed=5
            player.jump_height=9
        zg_main.parent=player
        auto_plane_ctrl.parent=player
        auto_plane_ctrl.enabled=False
        auto_plane_main.enabled=False
        camera.parent=player.camera_pivot
        plane_show_distance.enabled=False
        plane_show_pos.enabled=False
        plane_show_player_rotation.enabled=False
        plane_show_player_pos.enabled=False
        plane_show_zd.enabled=False
        ppsh41.enabled=True
        ptrd41.enabled=False
        f1.enabled=False
        show_plane_ctrl.color=color.white50
        player.wq=1
        invoke(Audio, 'plane_boom.ogg')
        plane_time.x-=1
        player.plane_audio.stop()
    if tiger_find.choose==True and distance(player,tiger_find)<20 and not player.on_t34:
        player.hp-=(20-int(distance(player,tiger_find)))*5
        be_hurt()
    if tiger_find.choose==True and distance(t34,tiger_find)<20:
        t34.life-=(20-int(distance(t34,tiger_find)))*100
        t34_be_hurt()
    if tiger_find.choose==True and distance(tiger_find,auto_plane_main)<20 and key_help.z==1:
        key_help.z=0
        camera.position=(0,0,0)
        camera.rotation=(0,0,0)
        if not player.on_t34:
            player.speed=5
            player.jump_height=9
        zg_main.parent=player
        auto_plane_ctrl.parent=player
        auto_plane_ctrl.enabled=False
        auto_plane_main.enabled=False
        camera.parent=player.camera_pivot
        plane_show_distance.enabled=False
        plane_show_pos.enabled=False
        plane_show_player_rotation.enabled=False
        plane_show_player_pos.enabled=False
        plane_show_zd.enabled=False
        ppsh41.enabled=True
        ptrd41.enabled=False
        f1.enabled=False
        show_plane_ctrl.color=color.white50
        player.wq=1
        invoke(Audio, 'plane_boom.ogg')
        plane_time.x-=1
        player.plane_audio.stop()
    if f1_find.choose==True and distance(player,f1_find)<15 and not player.on_t34:
        player.hp-=(15-int(distance(player,f1_find)))*5
        be_hurt()
    if f1_find.choose==True and distance(t34,f1_find)<15:
        t34.life-=(15-int(distance(t34,f1_find)))*40
        t34_be_hurt()
    if f1_find.choose==True and distance(f1_find,auto_plane_main)<15 and key_help.z==1:
        key_help.z=0
        camera.position=(0,0,0)
        camera.rotation=(0,0,0)
        if not player.on_t34:
            player.speed=5
            player.jump_height=9
        zg_main.parent=player
        auto_plane_ctrl.parent=player
        auto_plane_ctrl.enabled=False
        auto_plane_main.enabled=False
        camera.parent=player.camera_pivot
        plane_show_distance.enabled=False
        plane_show_pos.enabled=False
        plane_show_player_rotation.enabled=False
        plane_show_player_pos.enabled=False
        plane_show_zd.enabled=False
        ppsh41.enabled=True
        ptrd41.enabled=False
        f1.enabled=False
        show_plane_ctrl.color=color.white50
        player.wq=1
        invoke(Audio, 'plane_boom.ogg')
        plane_time.x-=1
        player.plane_audio.stop()
    if jump_time.y==0 and not player.on_t34:
        if player.wq==1 and held_keys['left mouse'] and show_ppsh41.on_cooldown==False and show_ppsh41.now_sl>0 and player.on_r==False and key_help.z==0 and player.on_eat==False:
            show_ppsh41.on_cooldown=True
            ppsh41_zd.enabled=True
            invoke(setattr, show_ppsh41, 'on_cooldown', False, delay=0.02)
            invoke(ppsh41_zd.disable, delay=.01)
            show_ppsh41.now_sl-=1
            invoke(Audio, 'jq.wav')
            if not player.left_ing:
                mouse.position=random.randint(-1,1)/120,random.randint(-1,1)/60
            else:
                mouse.position=random.randint(-1,1)/300,random.randint(-1,1)/180
    if player.wq==6 and show_t34_zd.sl!=0 and held_keys['left mouse'] and show_ppsh41.on_cooldown==False:
        show_ppsh41.on_cooldown=True
        ppsh41_zd.enabled=True
        invoke(setattr, show_ppsh41, 'on_cooldown', False, delay=0.05)
        invoke(ppsh41_zd.disable, delay=.01)
        invoke(Audio, 'jq.wav')
        show_t34_zd.sl-=1
    if camera.position==(0,0,0):
        zg_main.enabled=False
    else:
        zg_main.enabled=True
    if key_help.z==1 and not player.on_t34:
        auto_plane_1.rotation_y+=15
        auto_plane_2.rotation_y-=15
        auto_plane_3.rotation_y+=15
        auto_plane_4.rotation_y-=15
        camera.world_position=auto_plane_main.world_position-(0,0.5,0)
        camera.world_rotation=player.camera_pivot.world_rotation
        if held_keys['q']:
            if float(pow(10000-(player.x-auto_plane_help1.world_x)**2-(player.z-auto_plane_help1.world_z)**2,0.5))>auto_plane_main.y or player.god:
                auto_plane_main.y+=0.15
        if held_keys['e']:
            if float(pow(10000-(player.x-auto_plane_help1.world_x)**2-(player.z-auto_plane_help1.world_z)**2,0.5))>-auto_plane_main.y or player.god:
                auto_plane_main.y-=0.15
        if held_keys['w']:
            auto_plane_help.rotation_y=0+player.rotation_y
            if pow((player.x-auto_plane_help1.world_x)**2+(player.z-auto_plane_help1.world_z)**2+(player.y-auto_plane_help1.world_y)**2,0.5)<=100 or player.god:
                auto_plane_main.position=auto_plane_help1.world_position
        if held_keys['s']:
            auto_plane_help.rotation_y=180+player.rotation_y
            if pow((player.x-auto_plane_help1.world_x)**2+(player.z-auto_plane_help1.world_z)**2+(player.y-auto_plane_help1.world_y)**2,0.5)<=100 or player.god:
                auto_plane_main.position=auto_plane_help1.world_position
        if held_keys['a']:
            auto_plane_help.rotation_y=270+player.rotation_y
            if pow((player.x-auto_plane_help1.world_x)**2+(player.z-auto_plane_help1.world_z)**2+(player.y-auto_plane_help1.world_y)**2,0.5)<=100 or player.god:
                auto_plane_main.position=auto_plane_help1.world_position
        if held_keys['d']:
            auto_plane_help.rotation_y=90+player.rotation_y
            if pow((player.x-auto_plane_help1.world_x)**2+(player.z-auto_plane_help1.world_z)**2+(player.y-auto_plane_help1.world_y)**2,0.5)<=100 or player.god:
                auto_plane_main.position=auto_plane_help1.world_position
        if held_keys['left mouse'] and player.plane_zd>0 and auto_plane_main.on_cooldown==False:
            auto_plane_main.on_cooldown=True
            ppsh41_zd.enabled=True
            invoke(setattr, auto_plane_main, 'on_cooldown', False, delay=0.08)
            invoke(ppsh41_zd.disable, delay=.05)
            if mouse.hovered_entity and hasattr(mouse.hovered_entity,'hp_player') and not player.god:
                player.hp-=15
                key_help.z=0
                camera.position=(0,0,0)
                camera.rotation=(0,0,0)
                player.speed=5
                player.jump_height=9
                zg_main.parent=player
                auto_plane_ctrl.parent=player
                auto_plane_ctrl.enabled=False
                auto_plane_main.enabled=False
                camera.parent=player.camera_pivot
                plane_show_distance.enabled=False
                plane_show_pos.enabled=False
                plane_show_player_rotation.enabled=False
                plane_show_player_pos.enabled=False
                plane_show_zd.enabled=False
                ppsh41.enabled=True
                ptrd41.enabled=False
                f1.enabled=False
                show_plane_ctrl.color=color.white50
                player.wq=1
                player.plane_audio.stop()
                be_hurt()
            if mouse.hovered_entity and hasattr(mouse.hovered_entity,'hp_t34') and not player.god:
                t34.life-=1
                t34_be_hurt()
            invoke(Audio, 'jq.wav')
            player.plane_zd-=1
        if (raycast(auto_plane_main.position-(0,0.5,0), direction=(0,1,0), distance=1.2,ignore=(auto_plane_main,)).hit
            or raycast(auto_plane_main.position+(0,0.5,0), direction=(0,-1,0), distance=1.2,ignore=(auto_plane_main,)).hit
            or raycast(auto_plane_main.position, direction=(1,0,0), distance=1.7,ignore=(auto_plane_main,)).hit
            or raycast(auto_plane_main.position, direction=(-1,0,0), distance=1.7,ignore=(auto_plane_main,)).hit
            or raycast(auto_plane_main.position, direction=(0,0,1), distance=1.7,ignore=(auto_plane_main,)).hit
            or raycast(auto_plane_main.position, direction=(0,0,-1), distance=1.7,ignore=(auto_plane_main,)).hit
            ):
            if distance(t34,auto_plane_main)<15:
                t34.life-=30*(15-int(distance(t34,auto_plane_main)))
            key_help.z=0
            camera.position=(0,0,0)
            camera.rotation=(0,0,0)
            player.speed=5
            player.jump_height=9
            zg_main.parent=player
            auto_plane_ctrl.parent=player
            auto_plane_ctrl.enabled=False
            auto_plane_main.enabled=False
            camera.parent=player.camera_pivot
            plane_show_distance.enabled=False
            plane_show_pos.enabled=False
            plane_show_player_rotation.enabled=False
            plane_show_player_pos.enabled=False
            plane_show_zd.enabled=False
            ppsh41.enabled=True
            ptrd41.enabled=False
            f1.enabled=False
            show_plane_ctrl.color=color.white50
            player.wq=1
            if pow((player.x-auto_plane_main.x)**2+(player.z-auto_plane_main.z)**2,0.5)<3 and abs(player.y-auto_plane_main.y+0.25)<3:
                player.hp-=80
                be_hurt()
            invoke(Audio, 'plane_boom.ogg')
            plane_time.x-=1
            player.plane_audio.stop()
        plane_show_distance.text='distance:'+str(int(pow((player.x-auto_plane_main.x)**2+(player.z-auto_plane_main.z)**2+(player.y-auto_plane_main.y)**2,0.5)))
        plane_show_pos.text='plane_pos:'+str(int(auto_plane_main.x))+','+str(int(auto_plane_main.y))+','+str(int(auto_plane_main.z))
        plane_show_player_pos.text='player_pos:'+str(int(player.x))+','+str(int(player.y))+','+str(int(player.z))
        plane_show_player_rotation.text='plane_direction:'+str(int(camera.rotation_x))+','+str(int(camera.rotation_y))+','+str(int(camera.rotation_z))
        plane_show_zd.text='number of bullets:'+str(int(player.plane_zd))
    if player.air_time>0.1:
        player.will_hp-=0.05
    if player.grounded==True and player.will_hp!=0:
            if player.will_hp<=-2:
                be_hurt()
            invoke(Audio, 'fall.wav')
            player.hp+=int(player.will_hp)*5
            show_life.blink(color.red)
            show_life_background.blink(color.red)
            player.will_hp=0
    if key_help.z==2 or key_help.z==3:
        if hurt_show.color==color.rgba(0,0,0,0)  and not player.on_t34:
            player.speed=5
            player.jump_height=9
            key_help.z=0
    show_life.text='+'+str(int(player.hp))
    if not player.on_t34:
        if player.wq==4:
            show_time.text='number of times:'+str(int(plane_time.x))
        if player.wq==1:
            show_time.text='number of bullets:'+str(int(show_ppsh41.now_sl))+'/'+str(int(show_ppsh41.sl))
        if player.wq==2:
            show_time.text='number of bullets:'+str(int(show_ptrd41.now_sl))+'/'+str(int(show_ptrd41.sl))
        if player.wq==3:
            show_time.text='number of f1:'+str(int(show_f1.sl))
        show_t34_speed.enabled=False
        if held_keys['w'] or held_keys['s'] or held_keys['a'] or held_keys['d']:
            if player.camera_pivot.rotation_z>=0:
                player.camera_pivot.rotation_z=random.randint(-10,0)/50
            else:
                player.camera_pivot.rotation_z=random.randint(0,10)/50
                player.camera_pivot.y=1+random.randint(0,10)/1000
        else:
            player.camera_pivot.rotation_z=0
            player.camera_pivot.y=1
    else:
        if player.wq==5:
            show_time.text='number of main_gun:'+str(int(show_t34_cjd.sl))+'/∞'
        else:
            show_time.text='number of secondary_gun:'+str(int(show_t34_zd.sl))+'/∞'
        show_t34_life.text='+'+str(int(t34.life))
        show_t34_speed.text='t34_speed:'+str(round(t34.speed,2))
        show_t34_speed.enabled=True
def t34_be_hurt():
    show_t34_life.blink(color.red)
    show_t34_life_background.blink(color.red)
    show_t34_life_background.animate_color(color.rgba(41,77,84,100),delay=2)
    show_t34_life.animate_color(color.green,delay=2)
def be_hurt():
    key_help.z=2
    player.speed=0
    player.jump_height=0
    hurt_show.color=color.rgba(0,0,0,255)
    hurt_show.animate_color(color.rgba(100,0,0,250),duration=1,delay=0.75)
    hurt_show.animate_color(color.rgba(0,0,0,0),duration=10,delay=2)
    show_life.blink(color.red)
    show_life_background.blink(color.red)
    show_life_background.animate_color(color.rgba(41,77,84,100),delay=2)
    show_life.animate_color(color.rgba(26,41,85,200),delay=2)
def p_fire():
    p_fire_effect.color=color.rgba(255,255,0,255)
    p_fire_effect.animate_color(color.rgba(255,255,0,0),duration=0.1,delay=0.1)
app=Ursina()
the_sky=Sky()
stop_t34=Entity()
main_ground=Entity(model='cube',scale=(600,1,600),collider="box",texture='files/image/td.png',texture_scale=(600,600,600),position=(0,0,0))
main_ground2=Entity(model='cube',scale=(50,1,50),collider="box",texture='files/image/td.png',texture_scale=(50,50,50),position=(40,1,40),parent=stop_t34)
main_ground3=Entity(model='cube',scale=(50,1,50),collider="box",texture='files/image/td.png',texture_scale=(50,50,50),position=(80,2,80),parent=stop_t34)
jump_time=Entity()
key_help.input=key_input
player=FirstPersonController(x=-250,z=-250,hp=100,will_hp=0,plane_audio=Audio('fj.ogg',loop=True,autoplay=False,auto_destroy=False),t34_audio=Audio('fdj.ogg',loop=True,autoplay=False,auto_destroy=False),to_god=Audio('god.mp3',autoplay=False),plane_zd=300,wq=1,left_ing=False,on_r=False,on_eat=False,sl_food=5,god=False,on_t34=False,kill=0,died=False,win=False)
player.camera_pivot.y=1
zg_main=Entity(model='files/3d/zg/b.obj',parent=player,color=color.rgb(128,0,0),position=(0,0.9,0),collider='files/3d/zg/b.obj',hp_player=0)
zg_a=Entity(model='files/3d/zg/a.obj',parent=zg_main,color=color.rgb(255,255,77))
zg_c=Entity(model='files/3d/zg/c.obj',parent=zg_main,color=color.rgb(255,255,255))
zg_d=Entity(model='files/3d/zg/d.obj',parent=zg_main,color=color.rgb(0,0,0))
auto_plane_ctrl=Entity(model='files/3d/auto_plane/ctrl.obj',parent=player,scale=0.5,rotation_y=180,rotation_x=50,position=(0,0.5,1.5),enabled=False,hp_player=0)
auto_plane_main=Entity(model='files/3d/auto_plane/main_1.obj',scale=0.2,enabled=False,collider='files/3d/auto_plane/main_1.obj',on_cooldown=False)
auto_plane_1=Entity(model='files/3d/auto_plane/main_2.obj',parent=auto_plane_main,position=(3.55,-0.3,0))
auto_plane_2=Entity(model='files/3d/auto_plane/main_2.obj',parent=auto_plane_main,position=(-3.55,-0.3,0))
auto_plane_3=Entity(model='files/3d/auto_plane/main_2.obj',parent=auto_plane_main,position=(0,-0.3,3.55))
auto_plane_4=Entity(model='files/3d/auto_plane/main_2.obj',parent=auto_plane_main,position=(0,-0.3,-3.55))
plane_show_distance = Button(scale=(0.3,0.05),text_scale=20,text_color=color.white,text='text',position=(-0.5,0.46),enabled=False)
plane_show_pos = Button(scale=(0.3,0.05),text_scale=10,text_color=color.white,text='text',position=(-0.5,0.4),enabled=False)
plane_show_player_pos = Button(scale=(0.3,0.05),text_scale=10,text_color=color.white,text='text',position=(-0.5,0.34),enabled=False)
plane_show_player_rotation = Button(scale=(0.3,0.05),text_scale=10,text_color=color.white,text='text',position=(-0.5,0.28),enabled=False)
plane_show_zd = Button(scale=(0.3,0.05),text_scale=10,text_color=color.white,text='text',position=(-0.5,0.22),enabled=False)
show_time = Button(scale=(0.3,0.05),text_scale=10,text_color=color.white,text='text',position=(-0.5,-0.46))
hurt_show=Entity(model='quad',parent=camera.ui,color=color.rgba(0,0,0,0),scale=(2,1))
p_fire_effect=Entity(model='quad',parent=camera.ui,color=color.rgba(255,255,0,0),scale=(2,1))
show_life=Text(text='+100',color=color.rgba(26,41,85,200),scale=5,position=(0.45,-0.15))
show_life_background=Entity(model='quad',parent=show_life,color=color.rgba(41,77,84,100),scale=(0.06,0.05),position=(0.029,-0.01))
show_plane_ctrl=Entity(model='quad',parent=camera.ui,color=color.white50,scale=(0.2,0.15),position=(0.68,-0.4),texture='files/image/plane_ctrl.png')
show_f1=Entity(model='quad',parent=camera.ui,color=color.white50,scale=(0.1,0.15),position=(0.5,-0.4),texture='files/image/f1.png',sl=4,on_cooldown=False)
show_ptrd41=Entity(model='quad',parent=camera.ui,color=color.white50,scale=(0.25,0.15),position=(0.29,-0.4),texture='files/image/ptrd41.png',sl=10,now_sl=1)
show_ppsh41=Entity(model='quad',parent=camera.ui,color=color.white,scale=(0.25,0.15),position=(-0.01,-0.4),texture='files/image/ppsh41.png',sl=426,now_sl=71,on_cooldown=False)
auto_plane_help=Entity(parent=auto_plane_main)
auto_plane_help1=Entity(parent=auto_plane_help,position=(0,0,2))
ppsh41_zd=Entity(model='files/3d/ppsh41/ppsh41zd.obj',color=color.orange,scale=0.05,parent=camera,position=(0,0,5),enabled=False)
ptrd41_zd=Entity(model='files/3d/ptrd41/ptrd41zd.obj',color=color.orange,scale=0.05,parent=camera,position=(0,0,5),enabled=False)
player.cursor.enabled=False
player.gravity=1/6
player.jump_height=9
player.jump_up_duration=0.75
player.fall_after=3
the_sky.texture='files/image/the_sky.jpg'
ppsh41=Entity(model='ppsh41.obj',scale=0.05,parent=camera,position=(0.15,-0.1,0.35),color=color.orange,rotation_y=87)
ppsh41dj=Entity(model='ppsh41dj.obj',scale=1.2,parent=ppsh41,position=(-4.5,-2,0),color=color.dark_gray)
ptrd41=Entity(model='ptrd41.obj',scale=0.05,parent=camera,position=(0.15,-0.3,0.9),color=color.orange,rotation_y=87,enabled=False)
ptrd41d=Entity(model='ptrd41zd.obj',scale=0.3,parent=ptrd41,position=(0,4.7,0),color=color.orange,rotation_y=-90)
f1=Entity(model='f1a.obj',scale=0.05,parent=camera,position=(0.1,-0.3,0.5),color=color.gray,rotation_y=-45,enabled=False)
f1b=Entity(model='f1b.obj',parent=f1,color=color.brown)
tea=Entity(model='tea.obj',color=color.rgb(140,91,38),parent=camera,position=(-0.2,0,0.15),scale=0.05,rotation=(0,170,0),enabled=False)
food_long=Entity(model='food_long.obj',position=(0.1,0,0.15),scale=0.05,rotation=(-45,90,0),color=color.rgb(140,81,38),parent=camera,enabled=False)
fodd_main=Entity(model='food_main.obj',parent=food_long,color=color.white)
t34=Entity(model='t34d.obj',collider='t34d.obj',rotation_y=-90,color=rgb(0,42,0),position=(-200,3.3,-250),speed=0,scale=0.7,can_throw=False,life=5000,hp_t34=0)
t34pt=Entity(model='t34pt.obj',parent=t34,rotation_y=90,position=(0,1.8,3),collider='t34pt.obj',hp_t34=0)
player_t34_help=Entity(collider='box',position=(10,5.8,3))
t34p=Entity(model='t34p.obj',parent=t34pt,position=(-3,1.5,0),collider='t34p.obj',hp_t34=0)
show_t34_cjd=Entity(model='quad',parent=camera.ui,color=color.white,scale=(0.3,0.15),position=(0.29,0.4),texture='files/image/cjd.png',sl=1,on_cooldown=False,enabled=False)
show_t34_zd=Entity(model='quad',parent=camera.ui,color=color.white50,scale=(0.2,0.15),position=(0.59,0.4),texture='files/image/zd.png',sl=50,on_cooldown=False,enabled=False)
show_t34_speed = Button(scale=(0.3,0.05),text_scale=20,text_color=color.white,text='text',position=(-0.5,0.46),enabled=False)
show_t34_life=Text(text='+5000',color=color.green,scale=5,position=(0.35,0.15),enabled=False)
show_t34_life_background=Entity(model='quad',parent=show_t34_life,color=color.rgba(41,77,84,100),scale=(0.08,0.05),position=(0.035,-0.01))
Audio('space.ogg',loop=True,autoplay=True,auto_destroy=False)
for x in range(5):
    ju_87(position=(random.randint(900,1100),random.randint(70,150),random.randint(900,1100)))
y=1
x=250
z=250
m = Entity(model='cube', scale=(10, 1, 10), color=color.white, texture="td.png", texture_scale=(10, 10),collider="box", position=(x, y, z))
m = Entity(model='cube', scale=(10, 8, 1), color=color.white, texture="td.png", texture_scale=(10, 8),collider="box", position=(x, y + 3, z + 5))
m = Entity(model='cube', scale=(10, 8, 1), color=color.white, texture="td.png", texture_scale=(10, 8),collider="box", position=(x, y + 3, z - 5))
m = Entity(model='cube', scale=(1, 8, 10), color=color.white, texture="td.png", texture_scale=(10, 8),collider="box", position=(x + 5, y + 3, z))
m = Entity(model='cube', scale=(1, 8, 4), color=color.white, texture="td.png", texture_scale=(8, 4),collider="box",position=(x - 5, y + 3, z + 3))
m = Entity(model='cube', scale=(1, 8, 4), color=color.white, texture="td.png", texture_scale=(8, 4),collider="box",position=(x - 5, y + 3, z - 3))
m = Entity(model='cube', scale=(1, 4, 2), color=color.white, texture="td.png", texture_scale=(4, 2),collider="box",position=(x - 5, y + 6, z))
m = Entity(model='cube', scale=(10, 1, 8), color=color.white, texture="td.png", texture_scale=(10, 8),collider="box", position=(x, y + 6, z - 1))
m = Entity(model='cube', scale=(1, 1, 2), color=color.white, texture="td.png", texture_scale=(2, 1),collider="box",position=(x + 4, y + 6, z + 4))
m = Entity(model='cube', scale=(1, 1, 2), color=color.white, texture="td.png", texture_scale=(2, 1),collider="box",position=(x + 3, y + 5, z + 4))
m = Entity(model='cube', scale=(1, 1, 2), color=color.white, texture="td.png", texture_scale=(2, 1),collider="box",position=(x + 2, y + 4, z + 4))
m = Entity(model='cube', scale=(1, 1, 2), color=color.white, texture="td.png", texture_scale=(2, 1),collider="box",position=(x + 1, y + 3, z + 4))
m = Entity(model='cube', scale=(1, 1, 2), color=color.white, texture="td.png", texture_scale=(2, 1),collider="box",position=(x, y + 2, z + 4))
app.run()
