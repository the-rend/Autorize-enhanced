#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from javax.swing import JPanel
from javax.swing import JLabel
from java.awt import FlowLayout
from burp import IInterceptedProxyMessage

def addFilterHelper(typeObj, model, textObj):
        typeName = typeObj.getSelectedItem().split(":")[0]
        model.addElement(typeName + ": " + textObj.getText().strip())
        textObj.setText("")

def delFilterHelper(listObj):
        index = listObj.getSelectedIndex()
        if not index == -1:
                listObj.getModel().remove(index)

def modFilterHelper(listObj, typeObj, textObj):
        index = listObj.getSelectedIndex()
        if not index == -1:
                valt = listObj.getSelectedValue()
                val = valt.split(":", 1)[1].strip()
                modifiedFilter = valt.split(":", 1)[0].strip() + ":"
                typeObj.getModel().setSelectedItem(modifiedFilter)
                if ("Scope items" not in valt) and ("Content-Len" not in valt):
                        textObj.setText(val)
                listObj.getModel().remove(index)

def expand(extender, comp):
        if not hasattr(extender, 'requests_panel'):
                return
        for idx in range(extender.requests_panel.getTabCount()):
                if extender.requests_panel.getComponentAt(idx) == comp:
                        extender.requests_panel.setSelectedIndex(idx)
                        break
        extender.expanded_requests = 0

def collapse(extender, comp):
        rebuildViewerPanel(extender)

def _set_centered_tab_header(tabbed_pane, tab_index, title):
        header = JPanel(FlowLayout(FlowLayout.CENTER, 0, 0))
        header.setOpaque(False)
        header.add(JLabel(title))
        tabbed_pane.setTabComponentAt(tab_index, header)

def rebuildViewerPanel(extender):
        if not hasattr(extender, 'requests_panel'):
                return
        extender.requests_panel.removeAll()

        viewer_entries = []

        if hasattr(extender, 'user_viewers'):
                for user_id in sorted(extender.user_viewers.keys()):
                        key = 'user_{}'.format(user_id)
                        if extender.viewer_visibility.get(key, True):
                                viewer_entries.append((
                                        key,
                                        extender.user_viewers[user_id]['user_name'],
                                        extender.user_viewers[user_id]['panel']
                                ))

        if extender.viewer_visibility.get('original', True):
                viewer_entries.append(('original', 'Original', extender.original_requests_tabs))

        if extender.viewer_visibility.get('unauthenticated', True):
                viewer_entries.append(('unauthenticated', 'Unauthenticated', extender.unauthenticated_requests_tabs))

        for _, title, tabs in viewer_entries:
                extender.requests_panel.addTab(title, tabs)
                if title not in ('Original', 'Unauthenticated'):
                        _set_centered_tab_header(
                                extender.requests_panel,
                                extender.requests_panel.indexOfComponent(tabs),
                                title
                        )

        if extender.requests_panel.getTabCount() > 0:
                extender.requests_panel.setSelectedIndex(0)

        extender.requests_panel.revalidate()
        extender.requests_panel.repaint()
        extender.expanded_requests = 0

def handle_proxy_message(self,message):
        currentPort = message.getListenerInterface().split(":")[1]
        for i in range(0, self.IFList.getModel().getSize()):
            interceptionFilter = self.IFList.getModel().getElementAt(i)
            interceptionFilterTitle = interceptionFilter.split(":")[0]
            if interceptionFilterTitle == "Drop proxy listener ports":
                portsList = interceptionFilter[27:].split(",")
                portsList = [int(i) for i in portsList]
                if int(currentPort) in portsList:
                    message.setInterceptAction(IInterceptedProxyMessage.ACTION_DROP)