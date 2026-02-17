def world_to_screen(matrix, pos, width, height):
    # pos is (x, y, z)
    
    # Calculate Clip Coordinates
    clip_w = pos[0] * matrix[3] + pos[1] * matrix[7] + pos[2] * matrix[11] + matrix[15]

    # If w < 0.1, the enemy is behind you
    if clip_w < 0.1:
        return None

    # Calculate X and Y clip coordinates
    clip_x = pos[0] * matrix[0] + pos[1] * matrix[4] + pos[2] * matrix[8] + matrix[12]
    clip_y = pos[0] * matrix[1] + pos[1] * matrix[5] + pos[2] * matrix[9] + matrix[13]

    # Convert to Normalized Device Coordinates (NDC)
    ndc_x = clip_x / clip_w
    ndc_y = clip_y / clip_w

    # Final Screen Coordinates (FIXED)
    screen_x = (width / 2) + (ndc_x * width / 2)
    screen_y = (height / 2) - (ndc_y * height / 2)

    print(f"World: {pos} -> Screen: ({screen_x:.1f}, {screen_y:.1f})")
    return (int(screen_x), int(screen_y))