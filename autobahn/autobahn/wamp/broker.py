###############################################################################
##
##  Copyright (C) 2013-2014 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

from __future__ import absolute_import

from zope.interface import implementer

from autobahn import util
from autobahn.wamp import message
from autobahn.wamp.exception import ProtocolError, ApplicationError
from autobahn.wamp.interfaces import IBroker



@implementer(IBroker)
class Broker:
   """
   Basic WAMP broker, implements :class:`autobahn.wamp.interfaces.IBroker`.
   """

   def __init__(self):
      """
      Constructor.
      """
      ## map: session -> set(subscription)
      ## needed for removeSession
      self._session_to_subscriptions = {}

      ## map: session_id -> session
      ## needed for exclude/eligible
      self._session_id_to_session = {}

      ## map: topic -> (subscription, set(session))
      ## needed for PUBLISH and SUBSCRIBE
      self._topic_to_sessions = {}

      ## map: subscription -> (topic, set(session))
      ## needed for UNSUBSCRIBE
      self._subscription_to_sessions = {}


   def addSession(self, session):
      """
      Implements :func:`autobahn.wamp.interfaces.IBroker.addSession`
      """
      assert(session not in self._session_to_subscriptions)

      self._session_to_subscriptions[session] = set()
      self._session_id_to_session[session._my_session_id] = session


   def removeSession(self, session):
      """
      Implements :func:`autobahn.wamp.interfaces.IBroker.removeSession`
      """
      assert(session in self._session_to_subscriptions)

      for subscription in self._session_to_subscriptions[session]:
         topic, subscribers = self._subscription_to_sessions[subscription]
         subscribers.discard(session)
         if not subscribers:
            del self._subscription_to_sessions[subscription]
         _, subscribers = self._topic_to_sessions[topic]
         subscribers.discard(session)
         if not subscribers:
            del self._topic_to_sessions[topic]


   def processMessage(self, session, msg):
      """
      Implements :func:`autobahn.wamp.interfaces.IBroker.processMessage`
      """
      assert(session in self._session_to_subscriptions)

      if isinstance(msg, message.Publish):
         self._processPublish(session, msg)

      elif isinstance(msg, message.Subscribe):
         self._processSubscribe(session, msg)

      elif isinstance(msg, message.Unsubscribe):
         self._processUnsubscribe(session, msg)

      else:
         raise ProtocolError("Unexpected message {}".format(msg.__class__))


   def _processPublish(self, session, publish):

      if publish.topic in self._topic_to_sessions and self._topic_to_sessions[publish.topic]:

         ## initial list of receivers are all subscribers ..
         ##
         subscription, receivers = self._topic_to_sessions[publish.topic]

         ## filter by "eligible" receivers
         ##
         if publish.eligible:
            eligible = []
            for s in publish.eligible:
               if s in self._session_id_to_session:
                  eligible.append(self._session_id_to_session[s])
            if eligible:
               receivers = set(eligible) & receivers

         ## remove "excluded" receivers
         ##
         if publish.exclude:
            exclude = []
            for s in publish.exclude:
               if s in self._session_id_to_session:
                  exclude.append(self._session_id_to_session[s])
            if exclude:
               receivers = receivers - set(exclude)

         ## remove publisher
         ##
         if publish.excludeMe is None or not publish.excludeMe:
            receivers.discard(session)

      else:
         receivers = []

      publication = util.id()

      ## send publish acknowledge when requested
      ##
      if publish.acknowledge:
         msg = message.Published(session._my_session_id, publish.request, publication)
         session._transport.send(msg)

      ## if receivers is non-empty, dispatch event ..
      ##
      if receivers:
         if publish.discloseMe:
            publisher = session._my_session_id
         else:
            publisher = None
         # msg = message.Event(subscription,
         #                     publication,
         #                     args = publish.args,
         #                     kwargs = publish.kwargs,
         #                     publisher = publisher)
         for session in receivers:
            msg = message.Event(session._my_session_id,
                                subscription,
                                publication,
                                args = publish.args,
                                kwargs = publish.kwargs,
                                publisher = publisher)
            session._transport.send(msg)


   def _processSubscribe(self, session, subscribe):

      if True:

         if not subscribe.topic in self._topic_to_sessions:
            subscription = util.id()
            self._topic_to_sessions[subscribe.topic] = (subscription, set())

         subscription, subscribers = self._topic_to_sessions[subscribe.topic]

         if not session in subscribers:
            subscribers.add(session)

         if not subscription in self._subscription_to_sessions:
            self._subscription_to_sessions[subscription] = (subscribe.topic, set())

         _, subscribers = self._subscription_to_sessions[subscription]
         if not session in subscribers:
            subscribers.add(session)

         if not subscription in self._session_to_subscriptions[session]:
            self._session_to_subscriptions[session].add(subscription)

         reply = message.Subscribed(session._my_session_id, subscribe.request, subscription)

      else:
         reply = message.Error(session._my_session_id, message.Subscribe, subscribe.request, ApplicationError.INVALID_TOPIC)

      session._transport.send(reply)


   def _processUnsubscribe(self, session, unsubscribe):

      if unsubscribe.subscription in self._subscription_to_sessions:

         topic, subscribers = self._subscription_to_sessions[unsubscribe.subscription]

         subscribers.discard(session)

         if not subscribers:
            del self._subscription_to_sessions[unsubscribe.subscription]

         _, subscribers = self._topic_to_sessions[topic]

         subscribers.discard(session)

         if not subscribers:
            del self._topic_to_sessions[topic]

         self._session_to_subscriptions[session].discard(unsubscribe.subscription)

         reply = message.Unsubscribed(session._my_session_id, unsubscribe.request)

      else:
         reply = message.Error(session._my_session_id, message.Unsubscribe, unsubscribe.request, ApplicationError.NO_SUCH_SUBSCRIPTION)

      session._transport.send(reply)
