# python shooting game samaple
import pygame
import random
import sys

# 初期化
pygame.init()

# 画面設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Shooting Game")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# ゲーム設定
clock = pygame.time.Clock()
FPS = 60

# プレイヤークラス
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 50
        self.width = 60     # width = 幅
        self.height = 60    # height = 高さ
        self.speed = 10     # speed = 速度
        # 画像の読み込み(load)とサイズ変更(scale)
        img = pygame.image.load("neko.png")
        self.image = pygame.transform.scale(img, (self.width, self.height))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
     
    def draw(self, screen):
        # 画像の描画
        screen.blit(self.image, (self.x, self.y))

# 弾丸クラス
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.speed = 7
    
    def move(self):
        self.y -= self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
    
    def is_off_screen(self):
        return self.y < 0

# 敵クラス
class Enemy:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - 30)
        self.y = random.randint(-100, -30)
        self.width = 30
        self.height = 30
        self.speed = random.randint(2, 9)
    
    def move(self):
        self.y += self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
    
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

# 当たり判定関数
def check_collision(rect1_x, rect1_y, rect1_w, rect1_h, rect2_x, rect2_y, rect2_w, rect2_h):
    """矩形同士の当たり判定"""
    return (rect1_x < rect2_x + rect2_w and
            rect1_x + rect1_w > rect2_x and
            rect1_y < rect2_y + rect2_h and
            rect1_y + rect1_h > rect2_y)

# メインゲームループ
def main():
    player = Player()
    bullets = []
    enemies = []
    score = 0
    font = pygame.font.Font(None, 36)
    
    # 敵の出現タイマー
    enemy_timer = 0
    enemy_spawn_rate = 60  # 60フレームごとに敵出現
    
    running = True
    
    while running:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 弾を発射
                    bullet = Bullet(player.x + player.width // 2, player.y)
                    bullets.append(bullet)
        
        # キー入力処理
        keys = pygame.key.get_pressed()
        player.move(keys)
        
        # 弾の移動と削除
        for bullet in bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                bullets.remove(bullet)
        
        # 敵の出現
        enemy_timer += 1
        if enemy_timer >= enemy_spawn_rate:
            enemies.append(Enemy())
            enemy_timer = 0
        
        # 敵の移動と削除
        for enemy in enemies[:]:
            enemy.move()
            if enemy.is_off_screen():
                enemies.remove(enemy)
        
        # 弾と敵の当たり判定
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if check_collision(bullet.x, bullet.y, bullet.width, bullet.height,
                                 enemy.x, enemy.y, enemy.width, enemy.height):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10
                    break
        
        # プレイヤーと敵の当たり判定（ゲームオーバー）
        for enemy in enemies:
            if check_collision(player.x, player.y, player.width, player.height,
                             enemy.x, enemy.y, enemy.width, enemy.height):
                print(f"Game Over! Final Score: {score}")
                running = False
        
        # 描画
        screen.fill(BLACK)
        
        # オブジェクト描画
        player.draw(screen)
        
        for bullet in bullets:
            bullet.draw(screen)
        
        for enemy in enemies:
            enemy.draw(screen)
        
        # スコア表示
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # 操作説明
        help_text = font.render("Arrow keys: Move, Space: Shoot", True, WHITE)
        screen.blit(help_text, (10, SCREEN_HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

# メイン関数実行
if __name__ == "__main__":
    main()
