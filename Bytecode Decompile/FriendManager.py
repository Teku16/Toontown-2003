from ShowBaseGlobal import *
import DistributedObject, AvatarDNA, DirectNotifyGlobal

class FriendManager(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.__available = 0

    def setAvailable(self, available):
        self.__available = available

    def getAvailable(self):
        return self.__available

    def generate(self):
        if toonbase.tcr.friendManager != None:
            toonbase.tcr.friendManager.delete()
        toonbase.tcr.friendManager = self
        DistributedObject.DistributedObject.generate(self)
        return

    def disable(self):
        toonbase.tcr.friendManager = None
        DistributedObject.DistributedObject.disable(self)
        return

    def delete(self):
        toonbase.tcr.friendManager = None
        DistributedObject.DistributedObject.delete(self)
        return

    def up_friendQuery(self, inviteeId):
        self.sendUpdate('friendQuery', [inviteeId])
        self.notify.debug('Client: friendQuery(%d)' % inviteeId)

    def up_cancelFriendQuery(self, context):
        self.sendUpdate('cancelFriendQuery', [context])
        self.notify.debug('Client: cancelFriendQuery(%d)' % context)

    def up_inviteeFriendConsidering(self, yesNo, context):
        self.sendUpdate('inviteeFriendConsidering', [yesNo, context])
        self.notify.debug('Client: inviteeFriendConsidering(%d, %d)' % (yesNo, context))

    def up_inviteeFriendResponse(self, yesNoMaybe, context):
        self.sendUpdate('inviteeFriendResponse', [yesNoMaybe, context])
        self.notify.debug('Client: inviteeFriendResponse(%d, %d)' % (yesNoMaybe, context))

    def up_inviteeAcknowledgeCancel(self, context):
        self.sendUpdate('inviteeAcknowledgeCancel', [context])
        self.notify.debug('Client: inviteeAcknowledgeCancel(%d)' % context)

    def friendConsidering(self, yesNoAlready, context):
        self.notify.debug('Client: friendConsidering(%d, %d)' % (yesNoAlready, context))
        messenger.send('friendConsidering', [yesNoAlready, context])

    def friendResponse(self, yesNoMaybe, context):
        self.notify.debug('Client: friendResponse(%d, %d)' % (yesNoMaybe, context))
        messenger.send('friendResponse', [yesNoMaybe, context])

    def inviteeFriendQuery(self, inviterId, inviterName, inviterDna, context):
        dna = AvatarDNA.AvatarDNA()
        dna.makeFromNetString(inviterDna)
        self.notify.debug('Client: inviteeFriendQuery(%d, %s, dna, %d)' % (inviterId, inviterName, context))
        if inviterId in toonbase.localToon.ignoreList:
            self.up_inviteeFriendConsidering(4, context)
            return
        if not toonbase.localToon.acceptingNewFriends:
            self.up_inviteeFriendConsidering(6, context)
            return
        self.up_inviteeFriendConsidering(self.__available, context)
        if self.__available:
            messenger.send('friendInvitation', [inviterId, inviterName, dna, context])

    def inviteeCancelFriendQuery(self, context):
        self.notify.debug('Client: inviteeCancelFriendQuery(%d)' % context)
        messenger.send('cancelFriendInvitation', [context])
        self.up_inviteeAcknowledgeCancel(context)

    def up_requestSecret(self):
        self.sendUpdate('requestSecret', [])

    def requestSecretResponse(self, result, secret):
        messenger.send('requestSecretResponse', [result, secret])

    def up_submitSecret(self, secret):
        self.sendUpdate('submitSecret', [secret])

    def submitSecretResponse(self, result, avId):
        messenger.send('submitSecretResponse', [result, avId])