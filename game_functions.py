import sys
import os
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import pickle

def check_events(settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            f = open("high_score.txt", 'w')
            f.write(str(stats.high_score))
            f.close()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, stats, sb, aliens, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_keydown_events(event, settings, stats, sb, aliens, screen, ship, bullets):
    """ Respond to keypresses."""

    if event.key == pygame.K_LEFT:
        # Move the ship to the left
        ship.moving_left = True

    elif event.key == pygame.K_RIGHT:
        # Move the ship to the right
        ship.moving_right = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)

    elif event.key == pygame.K_r:
        reset_game(screen, stats, settings, sb, aliens, bullets, ship)

    elif event.key == pygame.K_q:
        # Store the high score before ending the game
        f = open("high_score.txt", 'w')
        f.write(str(stats.high_score))
        f.close()
        sys.exit()


def check_keyup_events(event, ship):
    """ Respond to key releases. """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False

    elif event.key == pygame.K_LEFT:
        ship.moving_left = False



def start_game(settings, screen, stats, sb, ship, aliens, bullets):
    # Reset the game settings.
    settings.initialize_dynamic_settings()
    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)
    # Reset the game statistics.
    stats.reset_stats()
    stats.game_active = True

    # Reset the scoreboard images. (make sure the scoring and level images are updated properly.)
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()


    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()

    # Create a new fleet and center the ship.
    create_fleet(settings, screen, ship, aliens)
    ship.center_ship()


def check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """ Start a new game if the button is clicked """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(settings, screen, stats, sb, ship, aliens, bullets)





def get_number_aliens_x(settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))

    return number_aliens_x

def get_number_rows(settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (settings.screen_height
                        - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number

    return alien

def create_fleet(settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    alien = Alien(settings, screen)
    number_aliens_x = get_number_aliens_x(settings, alien.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            alien = create_alien(settings, screen, aliens,
                    alien_number, row_number)
            aliens.add(alien)


def update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop

    screen.fill(settings.bg_color)

    ship.blitme()
    aliens.draw(screen)
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw()

    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def fire_bullet(settings, screen, ship, bullets):
    """ Fire a bullet if limit not reached yet. """
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)

def update_bullets(settings, screen, stats, sb, ship, aliens, bullets):
    """ Update position of bullets and get rid of old bullets."""
    # Update bullet positions
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    reward = check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets)

    return reward

def check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that collide
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True) # return a dictionary
    reward = 0   # set for DQN agent
    if collisions:
        for aliens in collisions.values():
            stats.score += settings.alien_points * len(aliens)
            reward += settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)


    if len(aliens) == 0:
        # Destroy existing bullets, speed up game, and create new fleet.
        # If the entire fleet is destroyed, start a new level
        bullets.empty()
        settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(settings, screen, ship, aliens)

    return reward

def check_fleet_edges(settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break

def change_fleet_direction(settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1

def ship_hit(settings, stats, sb, screen, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships left
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True) # make the mouse cursor visible again when the game ends.



def check_aliens_bottom(settings, stats, sb, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(settings, stats, sb, screen, ship, aliens, bullets)
            break



def update_aliens(settings, stats, sb, screen, ship, aliens, bullets):
    """
    Check if the fleet is at an edge, and then update the positions of all
    aliens in the fleet.
    """
    done = False # check if the ship collides with the aliens
    check_fleet_edges(settings, aliens)
    aliens.update() # this will automatically call each alien's update() method

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, sb, screen, ship, aliens, bullets)
        done = True

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(settings, stats, sb, screen, ship, aliens, bullets)

    return done

def check_high_score(stats, sb):
    """Check to see if there is a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def reset_game(screen, stats, settings, sb, aliens, bullets, ship):
    """Reset the game and start from the first level. This function is
       used for the learning agent.
    """
    stats.game_active = False
    sleep(1)
    start_game(settings, screen, stats, sb, ship, aliens, bullets)


def get_state(aliens, bullets, ship, reward, done):
    max_number_of_aliens = 16
    max_number_of_bullets = 3
    state = []

    for alien in aliens.sprites():
        state.extend(alien.rect[:2])

    state.extend([0] * 2 * (max_number_of_aliens - len(aliens.sprites())))

    for bullet in bullets.sprites():
        state.extend(bullet.rect[:2])

    state.extend([0] * 2 * (max_number_of_bullets - len(bullets.sprites())))
    state.extend(ship.rect[:2])
    state.append(reward)
    state.append(done)

    f = open('state.txt', 'wb')
    pickle.dump(state, f)
    f.close()
