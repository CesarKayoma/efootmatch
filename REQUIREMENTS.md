### The application will have the following entities

- Match
- Goal
- Player
- Team

### Entities and their attributes

#### 1. Match
- id
- man_of_the_match
- created_at

#### 2. Goal
- id
- scorer_id (FK player.id)
- assist_id (FK player.id)
- match_id (FK match.id)
- own_goal (bool)
- created_at

#### 3. Player
- id
- name
- team_id (FK team.id)
- created_at

#### 4. Team
- id
- name
- created_at

### Relationships

- One team has none or many players
- A player scores none or many goals
- A player assists none or many goals
- A match has none or many goals

### Business Rules

>BR01 - A Match must have a Man of the Match;<br>
>BR02 - A player must have a team; A player cannot exist if there are no teams available;<br>
>BR03 - A goal must be scored by a player; There can not be a goal without a player;<br>
>BR04 - A team cannot have more than one player with the same name; Thus, there can only be two Messi if they play for different teams;<br>
>BR05 - An own goal registered by one side must count as a goal scored by the other side; So, if Breno plays against César, and Breno's side scores an own goal, the player registered must be from Breno's side, but the goal must count towards César's side.<br>
>BR06 - A player cannot both score and assist the same goal<br>


### Functional Requirements

>FR01 - The system must allow the creation of new matches<br>
>FR02 - The system must allow the user to register new teams<br>
>FR03 - The system must allow the user to register new players<br>
>FR04 - The system must allow the registration of goals/assists of scored each match<br>
>FR05 - The system must show a timeline of the match events as the user register the goals<br>
>FR06 - The system must provide a dashboard displaying the main facts about the match<br>
>FR07 - The system must allow the user to view each match in detail<br>