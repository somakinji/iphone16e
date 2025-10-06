import pyxel

#背景ｸﾗｽ
class Background:
    NUM_STARS=10 #星の数

    #背景を初期化してｹﾞｰﾑに登録
    def __init__(self,game):
        self.game=game
        self.stars=[] #星の座標x,yと速度vx,vyのﾘｽﾄ

        for i in range(Background.NUM_STARS):
            x=pyxel.rndi(5,pyxel.width-5)
            y=pyxel.rndi(0,pyxel.height)
            vx=pyxel.rndf(-1,1)
            vy=pyxel.rndf(1,2)
            self.stars.append((x,y,vx,vy)) #ﾀﾌﾟﾙとしてﾘｽﾄに登録

        self.game.background=self  #ｹﾞｰﾑに背景を登録

    #背景を更新
    def update(self):
        for i,(x,y,vx,vy) in enumerate(self.stars):
            x +=vx
            if x>=pyxel.width-5: # code 13より
                x -=pyxel.width
            y +=vy
            if y>=pyxel.height:
                y -=pyxel.height
            self.stars[i]=(x,y,vx,vy)

    #背景を描画
    def draw(self):
        if self.game.scene !=Game.SCENE_TITLE: #title画面ではない時
            for x,y,vx,vy in self.stars:
                if 1<=vy and vy<1.3:
                    color=5 
                elif 1.3<= vy and vy<1.6:
                    color=10
                else: # 1.6=<vyの時
                    color=14 #vy速度が3つの範囲に応じて色を変える
                pyxel.pset(x,y,color)

#playerｸﾗｽ
class Player:
    LIFE_COUNT=5
    SHOT_INTERVAL=5

    def __init__(self,game,x,y):
        self.game=game
        self.x=x
        self.y=y
        self.hit_area=(2,1,5,5) #衝突範囲を緩めに変更
        self.shot_timer=0 #bullet発射迄の時間
        self.game.player=self #gameにplayerを登録
        pyxel.mouse(True) #mouse位置情報を表示する

    #playerのdamage受け関数
    def add_damage(self):
        self.game.life_count -=1 #damage受け後life_countを1つ減らす
        if self.game.life_count >0: #playerのlife_countが0でない場合
            Blast(self.game,self.x+4,self.y+4)
            pyxel.play(3,5)
        else: #playerのlife_countが0以下の場合
            Blast(self.game,self.x+4,self.y+4)
            self.game.player=None #blastｲﾍﾞﾝﾄ後playerにnone情報を代入
            pyxel.play(3,5)
            pyxel.stop()
            #change_scene関数にてsceneをgameoverに切替え
            self.game.change_scene(self.game.SCENE_GAMEOVER) 

            
    def update(self):
        self.x=pyxel.mouse_x-6 #mouse_x,mouse_y位置情報をself.x,self.yに代入
        self.y=pyxel.mouse_y-8
        self.x=max(self.x,0)
        self.x=min(self.x,pyxel.width-8)
        self.y=max(self.y,0)
        self.y=min(self.y,pyxel.height-8-8)
        
        if self.shot_timer>0: #bullet発射迄の時間がある場合
            self.shot_timer -=1 

        #mouse左ｸﾘｯｸし続け且つbullet発射待ち時間が0の場合
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.shot_timer==0:
            PlayerBullet(self.game,self.x,self.y,-90,4) 
            pyxel.play(3,3) #player bullet発射音ch=3,snd=3
            
            self.shot_timer=Player.SHOT_INTERVAL #shot_intervalをshot_timerに代入

        #mouse右ｸﾘｯｸし続け且つbullet発射待ち時間が0の場合
        elif pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT) and self.shot_timer==0:
            for i in range(0,15):
                PlayerBullet(self.game,self.x,self.y,i*15+165,4) 
                pyxel.play(3,3) #player bullet発射音ch=3,snd=3
                self.shot_timer=Player.SHOT_INTERVAL 
                
    def draw(self):
        pyxel.blt(self.x,self.y,1,0,0,7,8,0)

# injectionｸﾗｽ
class Injection:
    def __init__(self,game,x,y):
        self.game=game
        self.x=x
        self.y=y
        self.offset_x=0 #jetting左右方向の揺れ量
        self.offset_y=0 #jetting上下方向の揺れ量
        self.ship_direction=0 #playerが右へ移動(jetting左噴射):0 左へ移動:1 
        self.is_jetting_v=False
        self.is_jetting_h=False
        self.prev_mouse_x=pyxel.mouse_x
        self.prev_mouse_y=pyxel.mouse_y
        self.game.injection=self
        
    def update(self):
        self.x=pyxel.mouse_x-8+2
        self.y=pyxel.mouse_y+0

        self.x=max(self.x,0)
        self.x=min(self.x,pyxel.width-8)
        self.y=max(self.y,0)
        self.y=min(self.y,pyxel.height-8) #jettingが自機上限位置迄移動 bug???

        #prev_mouse_yとmouse_yが不一致の場合
        if pyxel.mouse_y !=self.prev_mouse_y: 
            self.is_jetting_v=True #jetting中(is_jettingにtrueを代入)
            self.prev_mouse_y=pyxel.mouse_y #現在値座標を次回のfrmのために保存
            self.offset_y=(pyxel.frame_count%3-0) if self.is_jetting_v else 0
        else: #rev_mouse_yとmouse_yが一致の場合(y方向停止の場合)
            self.is_jetting_v=False 

        #rev_mouse_xとmouse_xが不一致の場合
        if pyxel.mouse_x-self.prev_mouse_x >0:
            self.ship_direction=0
            self.is_jetting_h=True
            self.prev_mouse_x=pyxel.mouse_x #現在値座標を次回のfrmのために保存
            self.offset_x=(pyxel.frame_count%3-1) if self.is_jetting_h else 0
        #rev_mouse_xとmouse_xが不一致の場合
        elif pyxel.mouse_x-self.prev_mouse_x <0:
            self.ship_direction=1
            self.is_jetting_h=True
            self.prev_mouse_x=pyxel.mouse_x #現在値座標を次回のfrmのために保存
            self.offset_x=(pyxel.frame_count%3-1) if self.is_jetting_h else 0
        else: #rev_mouse_xとmouse_xが一致の場合(x方向停止の場合)
            self.is_jetting_h=False 
            
    def draw(self):
        if self.is_jetting_v: #jetting上下移動中の場合
            pyxel.blt(self.x,self.y+self.offset_y,1,0,8,8,8,0)
        else: 
            self.injection=None #injectionにnone情報を代入する

        if self.is_jetting_h: #jetting水平移動中の場合
            if self.ship_direction==0:
                pyxel.blt(self.x-8+self.offset_x,self.y-8,1,40,0,8,8+1,0)
            elif self.ship_direction==1:
                pyxel.blt(self.x-8+16-1+self.offset_x,self.y-8,1,56,0,8,8+1,0)
        else:
            self.injection=None

#enemyｸﾗｽ
class Enemy:
    TYPE_A=0
    TYPE_B=1
    SHOT_INTERVAL=90
    def __init__(self,game,type,level,x,y):
        self.game=game
        self.type=type #enemyの種類
        self.level=level #enemyの強さ
        self.x=x
        self.y=y

        self.hit_area=(1,1,5,6)
        self.armor=self.level-1

        self.mouth=0 #enemyのmouth(口パクパク)変数
        self.life_time=0
        self.shot_timer=0
        self.is_damaged=False
        self.game.enemies.append(self) #gameのenemyﾘｽﾄに登録する

    #enemyのdamage受け関数
    def add_damage(self): 
        if self.armor>0: #damageを受けた時 装甲がある場合
            self.armor -=1 #装甲を1減らす
            self.is_damage=True
            pyxel.play(3,4,resume=True)
            return #装add_damage関数終了
        
        
        Blast(self.game,self.x+4,self.y+4)
        pyxel.play(3,5,resume=True)
        
        if self in self.game.enemies:
            self.game.enemies.remove(self)
        self.game.score +=self.level*10

    def calc_player_angle(self):
        player=self.game.player
        if player is None:
            return 90
        else:
            return pyxel.atan2(player.y-self.y,player.x-self.x)

    def update(self):
        self.life_time +=1
        if self.shot_timer>0:
            self.shot_timer -=1

        if self.type==Enemy.TYPE_A:
            self.y +=0.5
            if self.life_time//60%2==0:
                self.x +=0.5
            else:
                self.x -=0.5

            if self.life_time%6==0 and self.shot_timer==0:
                player_angle=self.calc_player_angle()
                if player_angle >=0 and player_angle<=180: #player enemy間の角度が0-180度の時
                    EnemyBullet(self.game,self.x,self.y+8,player_angle,1)
                    pyxel.play(3,4) #enemyA bullet発射音ch=3,snd=4
                    self.shot_timer=Enemy.SHOT_INTERVAL
                else: #それ以外の角度の場合は何もしない(発射も含め)
                    pass

        elif self.type==Enemy.TYPE_B:
            self.y +=0.8

            if self.life_time%60==0 and self.shot_timer==0:
                for i in range(3):
                    EnemyBullet(self.game,self.x,self.y+8,i*45+45,1)
                    pyxel.play(3,4) #enemyB bullet発射音ch=3,snd=4
                    self.shot_timer=Enemy.SHOT_INTERVAL

        if pyxel.frame_count%2==0: #self.mouthを0,1繰返しによりenemyの口パクパク制御
            self.mouth=1-self.mouth

        if self.y>=pyxel.height-8 or self.x<=0 or self.x>=pyxel.width-8:
            if self in self.game.enemies:
                self.game.enemies.remove(self)

    def draw(self):
        if self.is_damaged:
            self.is_damaged=False
            for i in range(1,15):
                pyxel.pal(i,15)
            pyxel.blt(self.x,self.y,1,8,self.type*8,8,8,0)
        if self.mouth==0:
            pyxel.blt(self.x,self.y,1,8,self.type*8,8,8,0)
        else:
            pyxel.blt(self.x,self.y,1,16,self.type*8,8,8,0)
#弾ｸﾗｽ    
class PlayerBullet:
    
    def __init__(self,game,x,y,angle,speed):
        self.game=game
        self.x=x
        self.y=y
        self.vx=pyxel.cos(angle)*speed
        self.vy=pyxel.sin(angle)*speed
        
        self.hit_area=(1,0,5,4)
        game.playerbullets.append(self)
        
    def add_damage(self):
        if self in self.game.playerbullets:
            self.game.playerbullets.remove(self)
    
    def update(self):
        self.x +=self.vx
        self.y +=self.vy
        if (self.x<=-8 or self.x>=pyxel.width-8 or self.y<=-8 or self.y>=pyxel.height):
            self.game.playerbullets.remove(self)
            
    def draw(self):
        pyxel.blt(self.x,self.y,1,24,0,8,8,0)

class EnemyBullet:
    
    def __init__(self,game,x,y,angle,speed):
        self.game=game
        self.x=x
        self.y=y
        self.vx=pyxel.cos(angle)*speed
        self.vy=pyxel.sin(angle)*speed
        
        self.hit_area=(2,0,2,2)
        game.enemybullets.append(self)
        
    def add_damage(self):
        if self in self.game.enemybullets:
            self.game.enemybullets.remove(self)
    
    def update(self):
        self.x +=self.vx
        self.y +=self.vy
        if (self.x<=-8 or self.x>=pyxel.width-8 or self.y<=-8 or self.y>=pyxel.height):
            self.game.enemybullets.remove(self)
            
    def draw(self):
        pyxel.blt(self.x,self.y,1,32,0,8,8,0)

class Blast:
    START_RADIUS=1
    END_RADIUS=20
    MIDDLE_RADIUS=5
        
    def __init__(self,game,x,y):
        self.game=game
        self.x=x
        self.y=y
        self.radius=Blast.START_RADIUS
        game.blasts.append(self)

    def update(self):
        self.radius +=1
        if self.radius>Blast.END_RADIUS or self.radius>Blast.MIDDLE_RADIUS:
            self.game.blasts.remove(self)
        
    def draw(self):
        if self.game.life_count>0:
            self.radius=Blast.MIDDLE_RADIUS
        else:
            self.radius=Blast.END_RADIUS
        pyxel.circ(self.x,self.y,self.radius,7)
        pyxel.circb(self.x,self.y,self.radius,10)
        

def check_collision(entity1,entity2):
    entity1_x1=entity1.x+entity1.hit_area[0]
    entity1_y1=entity1.y+entity1.hit_area[1]
    entity1_x2=entity1.x+entity1.hit_area[2]
    entity1_y2=entity1.y+entity1.hit_area[3]

    entity2_x1=entity2.x+entity2.hit_area[0]
    entity2_y1=entity2.y+entity2.hit_area[1]
    entity2_x2=entity2.x+entity2.hit_area[2]
    entity2_y2=entity2.y+entity2.hit_area[3]

    if entity1_x1>entity2_x2:
        return False
    if entity1_x2<entity2_x1:
        return False
    if entity1_y1>entity2_y2:
        return False
    if entity1_y2<entity2_y1:
        return False
    return True



             
#ｹﾞｰﾑｸﾗｽ    
class Game:
    SCENE_TITLE=0
    SCENE_PLAY=1
    SCENE_GAMEOVER=2

    def __init__(self):
        pyxel.init(120,160,title="test")
        pyxel.load("assets/tohoho.pyxres") #ﾘｿｰｽﾌｧｲﾙの読込
        pyxel.mouse(True) #ﾏｳｽの表示
        self.scene=None
        self.score=0
        self.life_count=0
        self.background=None
        self.player=None
        self.injection=None
        self.enemies=[]
        self.playerbullets=[]
        self.enemybullets=[]
        self.blasts=[]
        self.play_time=0
        self.level=0
        
        Background(self) #Backgroundｲﾝｽﾀﾝｽを生成しBackgroudｸﾗｽのinit呼出し
        self.change_scene(Game.SCENE_TITLE)
        pyxel.run(self.update,self.draw)

    def change_scene(self,scene):
        self.scene=scene
        if self.scene==Game.SCENE_TITLE:
            #self.score=0 前回のscore履歴を残すため
            self.player=None
            self.injection=None
            self.enemies.clear()
            self.playerbullets.clear()
            self.enemybullets.clear()
            pyxel.playm(0,loop=True) #ｵｰﾌﾟﾆﾝｸﾞの曲msc=0

        elif self.scene==Game.SCENE_PLAY:
            self.score=0
            self.life_count=Player.LIFE_COUNT
            self.play_time =0
            self.level=1
            pyxel.playm(1,loop=True) #ﾌﾟﾚｲ中の曲msc=1
            Player(self,56,140) #self含む3つのparameter必要　???
            Injection(self,56,140)

        elif self.scene==Game.SCENE_GAMEOVER:
            self.display_timer=60 #60/30=2秒後にtitle画面にする
            self.player=None


    def update(self):
        self.background.update()

        if self.player is not None:
            self.player.update()
            self.injection.update()

        for enemy in self.enemies.copy():
            enemy.update()
            if self.player is not None and check_collision(self.player,enemy):
                self.player.add_damage()
                enemy.add_damage()
                
        for playerbullet in self.playerbullets.copy():
            playerbullet.update()

            for enemy in self.enemies.copy():
                if check_collision(enemy,playerbullet):
                    playerbullet.add_damage()
                    enemy.add_damage()
                    if self.player is not None:
                        self.player.sound_timer=5
        
        
        for enemybullet in self.enemybullets.copy():
            enemybullet.update()
            if self.player is not None and check_collision(self.player,enemybullet):
                enemybullet.add_damage()
                self.player.add_damage()
        
            for playerbullet in self.playerbullets.copy():
                playerbullet.update()

                if self.player is not None and check_collision(playerbullet,enemybullet):
                    playerbullet.add_damage()
                    enemybullet.add_damage()

        for blast in self.blasts.copy():
            blast.update()
        
        if self.scene==Game.SCENE_TITLE:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT): #ﾀｲﾄﾙ画面時にﾏｳｽ左ｸﾘｯｸした時
                pyxel.stop()
                self.change_scene(Game.SCENE_PLAY)

        elif self.scene==Game.SCENE_PLAY:
            self.play_time +=1
            self.level=self.play_time//300+1 #10秒毎にlevelに 1加算される
            spawn_interval=max(60-self.level*10,10) #10秒毎にspawn間隔が10frm変化する
            if self.play_time%spawn_interval==0:
                type=pyxel.rndi(Enemy.TYPE_A,Enemy.TYPE_B)
                Enemy(self,type,self.level,pyxel.rndi(0,120-8),-8)

        elif self.scene==Game.SCENE_GAMEOVER:
            if self.display_timer>0:
                self.display_timer -=1
            else:
                self.change_scene(Game.SCENE_TITLE)

    def draw(self):
        pyxel.cls(0)
        self.background.draw()

        if self.player is not None:
            self.player.draw()
            self.injection.draw()

        for enemy in self.enemies:
            enemy.draw()

        for playerbullet in self.playerbullets:
            playerbullet.draw()

        for enemybullet in self.enemybullets:
            enemybullet.draw()

        for blast in self.blasts:
            blast.draw()

        pyxel.text(10,4,f"SCORE{self.score:5}",7)
        pyxel.text(60,4,f"LIFE{self.life_count:5}",7)
        if self.scene==Game.SCENE_TITLE:
            pyxel.blt(40,50,2,0,0,32,32,15) #ﾀｲﾄﾙ画面の表示　仮作成中
            pyxel.text(20,120,"-PRESS MOUSE_LEFT-",7)

        
Game() #Gameｲﾝｽﾀﾝｽを生成しGameｸﾗｽのinit呼出し