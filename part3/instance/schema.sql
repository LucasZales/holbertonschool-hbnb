CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,

    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);


CREATE TABLE places (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,

    title VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    price FLOAT NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,

    owner_id VARCHAR(36) NOT NULL,

    CONSTRAINT fk_place_owner
        FOREIGN KEY (owner_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);


CREATE TABLE amenities (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,

    name VARCHAR(50) NOT NULL UNIQUE
);


CREATE TABLE reviews (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,

    text TEXT NOT NULL,
    rating INTEGER NOT NULL,

    place_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,

    CONSTRAINT fk_review_place
        FOREIGN KEY (place_id)
        REFERENCES places(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_review_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT unique_review
        UNIQUE (user_id, place_id)
);


CREATE TABLE place_amenity (
    place_id VARCHAR(36),
    amenity_id VARCHAR(36),

    PRIMARY KEY (place_id, amenity_id),

    CONSTRAINT fk_place_amenity_place
        FOREIGN KEY (place_id)
        REFERENCES places(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_place_amenity_amenity
        FOREIGN KEY (amenity_id)
        REFERENCES amenities(id)
        ON DELETE CASCADE
);
