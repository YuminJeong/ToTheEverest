# ToTheEverest!



https://youtu.be/0pis01MIKf8


![20230712_11542002](https://github.com/YuminJeong/ToTheEverest/assets/138415853/3ee0e8b2-1800-437d-8217-38baf9a93b92)
![화면 캡처 2023-07-12 115724](https://github.com/YuminJeong/ToTheEverest/assets/138415853/10d475df-b12c-4484-8e49-46ef9eae306f)
![화면 캡처 2023-07-12 115904](https://github.com/YuminJeong/ToTheEverest/assets/138415853/29dfe785-f77d-417d-9a15-db1613708699)
![화면 캡처 2023-07-12 115958](https://github.com/YuminJeong/ToTheEverest/assets/138415853/966286af-b304-475c-8c03-9a2a2d32bc55)
![20230712_11555635](https://github.com/YuminJeong/ToTheEverest/assets/138415853/dc1a1022-479a-4225-b27e-0bdea2d47351)






This is a jumping flatformer game with Doodle Jump as a reference.
The player jumps up while stepping on the platform.
I chose the main character as a snowman.
The snowman is crying because it is melting because it is in such a hot area. We have to raise this snowman to Everest and make it not melt.
The snowman moves left when the player presses A, right when the player presses D, and jumps when the space bar is pressed.
Whenever a snowman steps on the platform and jumps, the height of the snowman is updated by 100m and displayed in the upper left of the screen.
Also, the time it takes for a snowman to reach the top of the mountain is indicated in second.
Players can have fun recording how fast they reach the top of the mountain.
In order to climb faster, the snowman has to get an item.
If you acquire a scarf item that appears in between, the height that a snowman can jump will be 1.5 times higher than before.
After 3 seconds, you will return to the original jump height, so you will have to acquire the item again.
When the snowman reaches the top, the crying snowman turns into a smiling face, and a happy song comes out.

        if self.player.rect.top < HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top > HEIGHT:
                    if self.background_position.y < -100:
                        self.PLAYER_SCORE += 100
                        print(self.PLAYER_SCORE)
                        plat.kill()
                        self.background_position.y += abs(self.player.vel.y) * 5
                    else:
                        self.player.pos.y += 0
                        self.PLAYER_SCORE = 8849
                        self.background_position.y += 0
Everest is 8849 meters tall. However, since it increases by 100m every time you step on the platform, it is set to automatically update to 8849m when the y-coordinate of the background image reaches -100.
Similarly, we made m and second updates stop when the y coordinates of the background image reach -100.

         if self.player.rect.top < HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top > HEIGHT:
                    if self.background_position.y < -100:
                        self.PLAYER_SCORE += 100
                        print(self.PLAYER_SCORE)
                        plat.kill()
                        self.background_position.y += abs(self.player.vel.y) * 5
                    else:
                        self.player.pos.y += 0
                        self.PLAYER_SCORE = 8849
                        self.background_position.y += 0
The y value of the background image image was added as 5 times as 5 times.
