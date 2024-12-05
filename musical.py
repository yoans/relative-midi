import pygame
import pygame.midi
import time
import sys

class MusicalKeyboard:
    def __init__(self):
        # Initialize Pygame and Pygame MIDI
        pygame.init()
        pygame.midi.init()

        # Set up the display
        self.screen = pygame.display.set_mode((400, 200))
        pygame.display.set_caption("Musical Keyboard Game")

        # Set up MIDI output
        self.midi_out = pygame.midi.Output(pygame.midi.get_default_output_id())
        
        # Define key mappings and their corresponding half-step modifications
        self.key_mappings = {
            pygame.K_a: -4,   # 'a' key: down 4 half steps
            pygame.K_s: -3,   # 's' key: down 3 half steps
            pygame.K_d: -2,   # 'd' key: down 2 half steps
            pygame.K_f: -1,   # 'f' key: down 1 half step
            pygame.K_SPACE: 0,# space: no change
            pygame.K_j: 1,    # 'j' key: up 1 half step
            pygame.K_k: 2,    # 'k' key: up 2 half steps
            pygame.K_l: 3,    # 'l' key: up 3 half steps
            pygame.K_SEMICOLON: 4  # ';' key: up 4 half steps
        }

        # Initial note settings
        self.current_note = 60  # Middle C
        self.last_key = None
        self.channel = 0
        self.volume = 127

    def play_note(self, note):
        # Turn off the previous note
        self.midi_out.note_off(self.current_note, self.volume, self.channel)
        
        # Play the new note
        self.midi_out.note_on(note, self.volume, self.channel)
        self.current_note = note

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    # Check if the pressed key is in our mappings
                    if event.key in self.key_mappings:
                        # Calculate the new note based on the half-step modification
                        half_steps = self.key_mappings[event.key]
                        new_note = self.current_note + half_steps
                        
                        # Play the new note
                        self.play_note(new_note)
                        
                        # Store the last key pressed
                        self.last_key = event.key
                    
                    # If the key is not in mappings, repeat the last key
                    elif self.last_key is not None:
                        half_steps = self.key_mappings[self.last_key]
                        new_note = self.current_note + half_steps
                        self.play_note(new_note)

            # Update the display
            self.screen.fill((255, 255, 255))
            font = pygame.font.Font(None, 36)
            text = font.render(f"Current Note: {self.current_note}", True, (0, 0, 0))
            self.screen.blit(text, (50, 80))
            pygame.display.flip()

        # Clean up
        pygame.midi.quit()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = MusicalKeyboard()
    game.run()