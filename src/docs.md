# Documentation for Isaac
## Author: doncato / don.cato.dc11@gmail.com / https://github.com/doncato
## doc v. 0.4 / isc v. 2.5

## Isaac facts
Isaac was written by me (doncato, contact information listed above),
the current script for Isaac was first created on the 27th January of 2020
Isaac is my main discord.py project, which was first named Catherine (from Soma) in 2019
which turned then to Isaac (without any reference). Isaac theme and character is supposed
to be annoyed or cynical.
Some Commands will get a reaction (in form of a check mark) this indicates a success and it's important
to know that this reaction is typically the last thing that is done in a command.


## Events
Isaac will respond to different events on the server:

+ status change
    if a member switches from online/dnd to idle/offline while being connected to a voice channel,
    Isaac will mute that user, as it's assumed that the user is now inactive. This is to avoid
    disruption of the voice chat and humiliation of the inactive user. If a user switches back from
    offline/idle to online/dnd while being in a voice channel, the user will also be unmuted **IF**
    he was previously muted by the bot itself. (That way it should **NOT** be possible to abuse this feature
    to unmute yourself without proper permission)

    Yet there's no way to configure this behaviour, but this will be changed somewhen. 
+ ban
    if a member gets banned, there will be a reaction in the system channel
    this event can be customized in the setting "send_ban_msg"
+ unban
    if a member gets her/his ban revoked, there will be a reaction in the system channel
    this event can be customized in the setting "send_unban_msg"
+ join
    if a member joins the server, there will be a reaction in the system channel
    this event can be customized in the setting "send_welcome_msg"
+ command error
    if an error occurs after submitting a command, it will pass the straight error message
    from python / discord.py to the channel where the error occured, this is also called
    'lazy error handling', however it might be, that an error is caused by a bug in which
    case there's little for you to do but submitting the bug to me (or any devs)

## 'Passives'
Passive abilities of Isaac which require no explicit Command

### Automatic voice channel management
If a voice channel exists which starts with the greek letter ?? (Mu) and the voice channel
has the user limit set to 1,2 or 3, the bot will duplicate that voice channel, change the name, set the bitrate
of that channel to 8 kbit/s, the user limit to 0 / infinite and move the joined member to that newly made channel.
The bitrate of that channel will remain 8 kbit/s as long as 1 member is in that channel, with more members the bitrate
will be set to 56 kbit/s if all member left the voice channel will be deleted after 1 sec delay (joining the channel
during the delay will not abort or extend the deletion). The name of the voice channel will be set to the following formats:

+ if the member is playing something
    {Gamename}-{Nickname}-??
+ else
    {Greek letter}-{Integer}-{Nickname}-??

_Notes:_
    Greek letter is a random greek letter and Integer is a random number between 10 and 99 (endpoints included).
    There's no backcheck if the random created names aren't already existent!
    (But duplicates are not probable and shouldn't be problematic)
    The channelname won't change during use.
Isaac will detect the behaviour of the voice channels by the name a ?? at the beginning of the name means to create
voice channels upon join and a ?? at the end of the name tells Isaac to manage this voice channel's bitrate and deletion


## Commands
All commands will return the message in the discord.embed format, the color is in most cases the same
color that the bot is displayed with (aka. it's main role color)

### Core Commands (core)

#### load - reload(self, ctx)
The load command requires no arguments, and will (re)load all extensions. Every class, except for the core class is an extension.
This command will go through every python file, that is in the same directory as the core file and try to load all classes as an extension.
Important Note: If one file fails to load, the process will be interrupted and no further classes will be loaded!
Therefore the bot only needs a restart if the core file needs to be edited (which is unlikely to be necessary).

#### stat - info(self, ctx)
The stat command requires no arguments, it will return the latency of the bot in milliseconds, the time
since the script was started, the current version and the release date of the current version. This command
can be used to check if the bot is alive.


### System Commands (system)

#### get-docs - docs(self, ctx):
The get-docs command requires no arguments and has a cooldown of 5 min, it'll upload this text file with the
official documentation of Isaac

#### manager_vc - vcmanage(self, ctx)
This command will just return a text explaining the automatic voice channel management.

#### autoroles - autoroles(self, ctx, action="show", message_id=0, emoji='', roles_id=0, channel_id=0)
This command is used to set and configure the autoroles function,
meaning when a User reacts to a specific message with a specific emoji;
That user will get a specific role, if possible.
There are 3 Actions:

+ show (default) - will show current react-rules
+ add - will add a specific rule with given message-id, emoji and role-id
+ remove - will remove a specific rule with given message-id and emoji

_Notes:_
    There's no backcheck if the rules are correctly set, if the rules
    are incorrect the role won't be given upon reaction!
    The channel-id argument is only for the bot to react on the message when __adding__
    a role, the channel-id is not saved, so leaving it blank won't make a difference
    in functionality

#### set setting(self, ctx, setting=None, value=None)
The set command requires Administrative permissions. It will set the server settings for Isaac
you can specify the setting to change with the setting argument and determine it's value with the value argument.
Isaac should return an error if the setting is not found.
You can check the available settings by leaving settings and value to it's defaults and
get the current value of a setting by specifying a setting but no value.

_Notes:_
    There's no backcheck if your settings are correct so pay attention to their values!
    Channels or Roles should be pinged or their ID should be set.
    Other fields (like send_welcome_msg) can be answered with custom content, or be disabled
    by inserting a '.'
    Booleans can be answered with anything that starts with 'y' or 't' for enabled
    anything else will lead to disabled or defaults.

### Owner Bug report (owner_mail)

#### buglist - buglist(self, ctx)
The buglist command should only be used by the bot owner (me), it will list all known bugs by priority. As each element
will be a link pointing to the message of the bot, it will only be useful for the owner (me)
#### bug - bug(self, ctx, *description)
The bug command can be used to report bugs to the bot owner (me), it is possible to provide attachments! Try to provide as much
information on a bug as possible as this will increase the chance of a soon fix! The owner will get notified and can react to your
submission, you'll get notified once this happens!

### Fun commands (fun)

#### judge - judge(self, ctx, *user)
The judge command will return an embed of user information to a mentioned user, it'll only return information to one user
at a time and it will never accept itself as user.
The information will contain the Nickname, Username, Usertag, profile Picture, if the user is a bot or not, current profile badges
and the roles the user has. The color of the embed will match the color of the user.

#### rename-madness - rename(self, ctx, scheme='custom', *words)
This command will change the nickname of every user on the server, it requires the 'manage nicknames' permission
There are existent schemes for the rename but custom ones are possible.
Note that you always need at least as much names/words as there are users on the server
Possible schemes are:

+ custom:
    Provide the words afterwards, seperated by spaces, to use for the rename
+ numerical:
    Just simple decimal numbers (has no limit)
+ binary:
    binary numbers as usernames (has no limit)
+ hexadecimal:
    hexadecimal numbers as usernames (has no limit)
+ fuck:
    will repeat the provided word with every user (if input word set to '_', user1 will be '_', user2 = '__', user3 = '___' and so on)(has no limit)
+ reset:
    will reset all usernames (has no limit)
+ latin:
    latin/german letters as usernames (limit determined by the length of the alphabet)
+ greek:
    greek letters as usernames (limit determined by the length of the alphabet)
+ phonetic:
    the nato phonetic alphabet as usernames (limit determined by the length of the alphabet)

_Notes:_
    'has no limit' means that every username could be changed as the scheme is infinitely extendable,
    however the limit of 32 characters for the username still applies and it's not possible to change the usernames of users with higher authority than
    the bot itself.

#### vc - vc(self, ctx, command='join', category='', *track)
The vc command is a voice chat implementation for Isaac, you can determine Isaac's action(s) with the command argument.
Following commands are possible:

+ join:
    will connect the bot to the voice channel the user is currently in
+ disconnect:
    will disconnect the bot from a voice channel
+ volume:
    will set the volume serverwide, this can also be set through the 'set' command
    by leaving the category empty the current volume can be displayed
+ play:
    play a voice line which must be provided in the external .json file. You can provide the category and the voice lines (track) with the arguments.
    This has already a search function build in, so the names should not get in your way, empty fields will result in a random line.
    You can also search in all categories by using '*' as category, it'll always pick the first occurence that it finds.
+ stop:
    will stop any current playback

#### glitch - glitch(self, ctx, user=None, amount=100, file_format='png', amount_change=10)
The glitch command will glitch the profile picture of a mentioned user. The picture will be a gif if file_format set to 'gif'
the amount is the amount of the glitch effect and the amount_change will be the change of the amount between each frame of the gif.

_Notes:_
    This command might not work with already animated profile pictures

### Admin commands (admin)

#### mu - mu(self, ctx, *users)
The mu command requires administrative permissions and will server-mute any mentioned users that are connected to a voice channel
You can provide multiple users and also multiple roles at the same time, wich will server-mute each member of the provided Roles
This command toggles the server-mute, already muted people, will be unmuted afterwards

#### de - de(self, ctx, *users)
The de command is the same as the 'mu' command but will server-deaf the users.
