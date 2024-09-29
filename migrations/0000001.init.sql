create table authors (
    id bigserial primary key,
    name text not null
);

create table books (
    id bigserial primary key,
    title text not null,
    author_id bigint not null references authors(id) on delete cascade
);

create index books_author_id_idx on books (author_id);

insert into authors (name) values ('Oscar Wilde'), ('Agatha Christie'), ('Mark Twain');
insert into books (title, author_id) values 
    ('The Picture of Dorian Gray', (select id from authors where name = 'Oscar Wilde')),
    ('An Ideal Husband', (select id from authors where name = 'Oscar Wilde')),
    ('Poetry', (select id from authors where name = 'Oscar Wilde')),
    ('The Man in the Brown Suit', (select id from authors where name = 'Agatha Christie')),
    ('The Mysterious Affair at Styles', (select id from authors where name = 'Agatha Christie')),
    ('The Adventures of Tom Sawyer', (select id from authors where name = 'Mark Twain')),
    ('The Adventures of Huckleberry Finn', (select id from authors where name = 'Mark Twain'));
