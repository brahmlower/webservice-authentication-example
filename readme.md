
# Authenticated Buildings API

## Project Background

This project is a case study in tying various authentication methods together
around a central user account, and providing functionality on the aggregate
identity data. Inspiration for this project stems from several sources:

- Simple account implementations at work
- Frustrations on managing multiple personal acounts on services (creds vs oauth provider)
- Plain ol' curiosity (What's it like to integrate with an oauth provider? To provide 2FA? Sms/email verification?)

Before jumping into the project, I did a little bit of cursory research on
existing best practices. Most roads pointed back to various OWASP resources, most
of which are distilled in their
[various](https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Forgot_Password_Cheat_Sheet.md)
[authentication](https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Authentication_Cheat_Sheet.md)
[cheetsheets](https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Password_Storage_Cheat_Sheet.md).
This project is split into several phases to help keep focused while in
development:

1. Basic platform

    Get decently designed frontend and backend put together, mocking out some
    buisiness need, and providing end user controls (login, logout, account
    management interfaces)

2. Standard Authentication

    Implement details around username/password authentication. Beyond hashing
    credentials, this involves supporting migrating hashing strategies, denoting
    force password resets, user initiated account merges

3. Oauth provider integration

    Support as many third party Oauth providers as I can. Google, Facebook and
    Github are the common providers I've seen, but others like Auth0, Playstation
    network, Xbox?, Microsoft?, Amazon?. There's a ton out there, and I'm sure
    they all work nearly identically, but if I can find even 1 that's significantly
    different than the rest, the quantity will be worth it.
4. 2FA & Recovery keys
    I expect this phase to be the most broad, as the various options for 2FA can
    require significantly different mechanisms for authentication. The methods I
    plan to implement are SMS, Email, Due, Google Authenticator, YubiKey and
    printable recovery keys. I want to note that SMS and Email would be implemented
    only because they're common strategies I've seen offered, even though both
    are considered insecure options for 2FA.

If you poke through the codebase at this point, you will notice that scafolding
and partial implementations are already in place for a couple phases- these were
from basic proof of concept tests before I built a proper project timeline.

### Phase 1 Update

At this time, phase 1 is nearly complete. The UI for basic account management
processes needs to be finished, but aside from that, **super** basic platform
functionality has been implemented or mocked. A decent portion of phase 2 has
been completed or partially implemented. So once phase 1 is finished, most of the
work will be in solidifying tests and tying API endpoints to UI components.

## Project Structure

The project layout is relatively self explainitory, but it's worth covering:

- /backend

    Python package for the backend api lives here. This directory contains all
    the build assets needed for the python package as well as the docker image
    used as the final delivery artifact.

- /docker

    This project uses a simple nginx container to serve static frontend assets
    and to proxy api requests along to the backend service. The nginx
    configurations live in this directory and are mounted in as volumes by
    docker-compose.

- /frontend

    React source and assets live in here. This was bootstraped by the create-react-app
    utility.

- /sql

    Sqitch is used as a general SQL migrations manager, and as such, this directory
    structure is largely dictated by sqitch. The makefile is useful for executing
    common actions without having to invest too much time in remembering sqitch
    usage.

### Makefiles

I tend to use makefiles as an entrypoint user interface during development. Most
common tasks are writen out in a makefile for easy execution, and for reference.
You'll notice that the toplevel makefile itself hardly does anything original- it
just calls out to the makefiles in the various subdirectories. If you're unsure
about what can be done in some directory, running `make help` or looking at the
makefile is a great first step in getting familiarized.

## Setup & Build

Project dependencies:
- Docker
- Docker Compose
- [Sqitch](https://sqitch.org/)
- Python3 (including pip, virtualenv)
- Make
- NPM
- React

### Backend

The backend is set up as a single package that gets installed in a docker image,
which keeps the initial installation process relatively simple.

```
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ make backend-build
$ docker-compose build api
```

### Frontend

The frontend build process is pretty simple as far as NPM projects go- just cd
into the directory, install and build. Disclaimer: I'm not a frontend dev by
interest, so I haven't invested as much time in learning about, improving, or
cleaning up this build process.

```
cd frontend
npm install
npm run build
```

### Database

The makefiles aim to make applying and reverting sqitch migrations as easy as
possible. You should be able to start the postgres container, and apply the
migrations using the following two steps:

```
docker-compose up -d db
make deploy
```

If you want to revert the database, you can destroy the container volume, or run

```
make revert
```

### The full stack

If you've completed the build process for the previous three sections (backend,
frontend, and database), then you should be able to bring up all the docker
containers and visit the site locally.

```
docker-compose up -d
```
