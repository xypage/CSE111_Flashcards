CREATE TABLE "Flashcard"(id INTEGER NOT NULL, PRIMARY KEY(id));

CREATE TABLE "Side"(
  id INTEGER NOT NULL,
  "Header" TEXT NOT NULL,
  "Body" INTEGER,
  "Image" INTEGER,
  "Flashcard_id" INTEGER NOT NULL,
  PRIMARY KEY(id),
  CONSTRAINT "Flashcard_Side"
    FOREIGN KEY ("Flashcard_id") REFERENCES "Flashcard" (id)
);

CREATE TABLE "Deck"(id INTEGER NOT NULL, PRIMARY KEY(id));
