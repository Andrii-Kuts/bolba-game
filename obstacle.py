
from player import Player

PADDING = 1

class Obstacle:
    def __init__(self, l, r, d, u):
        self.l = l
        self.r = r
        self.u = u
        self.d = d

    def limitX(self, player: Player, vx):
        pu = player.y + player.radius
        pd = player.y - player.radius
        pl = player.x - player.radius
        pr = player.x + player.radius
        if pu <= self.d or pd >= self.u:
            return vx
        
        if vx > 0:
            d = self.l - pr
            if d < 0:
                return vx
            return min(vx, d - PADDING)
        else:
            d = self.r - pl
            if d > 0:
                return vx
            return max(vx, d + PADDING)
        
    def limitY(self, player: Player, vy):
        pu = player.y + player.radius
        pd = player.y - player.radius
        pl = player.x - player.radius
        pr = player.x + player.radius
        if pr <= self.l or pl >= self.r:
            return vy
        
        if vy > 0:
            d = self.d - pu
            if d < 0:
                return vy
            return min(vy, d - PADDING)
        else:
            d = self.u - pd
            if d > 0:
                return vy
            return max(vy, d + PADDING)
        