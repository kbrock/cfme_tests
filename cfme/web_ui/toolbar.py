"""A set of functions for dealing with the toolbar buttons

The main CFME toolbar is accessed by using the Root and Sub titles of the buttons.

Usage:

    tb = web_ui.toolbar
    tb.select('Configuration', 'Add a New Host')

"""
import cfme.fixtures.pytest_selenium as sel
from selenium.webdriver.common.by import By


def root_loc(root):
    """ Returns the locator of the root button

    Args:
        root: The string name of the button.
    Returns: A locator for the root button.
    """
    return (By.XPATH,
        "//div[contains(@class, 'dhx_toolbar_btn')][contains(@title, '%s')]" % root)


def sub_loc(sub):
    """ Returns the locator of the sub button

    Args:
        sub: The string name of the button.
    Returns: A locator for the sub button.
    """
    return (By.XPATH, "//div[contains(@class, 'btn_sel_text')][contains(., '%s')]/../.." % sub)


def select_n_move(el):
    """ Clicks an element and then moves the mouse away

    This is required because if the button is active and we clicked it, the CSS class
    doesn't change until the mouse is moved away.

    Args:
        el: The element to click on.
    Returns: None
    """
    # .. if we don't move the "mouse" the button stays active
    sel.click(el)
    sel.move_to_element((By.XPATH, '//div[@class="brand"]'))


def select(root, sub=None, invokes_alert=False):
    """ Clicks on a button by calling the :py:meth:`click_n_move` method.

    Args:
        root: The root button's name as a string.
        sub: The sub button's name as a string. (optional)
        invokes_alert: If ``True``, then the behaviour is little bit different. After the last
            click, no ajax wait and no move away is done to be able to operate the alert that
            appears after click afterwards. Defaults to ``False``.
    Returns: ``True`` if the button was enabled at time of clicking, ``False`` if not.
    """
    if not is_greyed(root):
        if sub is None and invokes_alert:
            # We arrived into a place where alert will pop up so no moving and no ajax
            sel.click(root_loc(root), wait_ajax=False)
        else:
            select_n_move(root_loc(root))
    else:
        return False
    if sub:
        if not is_greyed(root, sub):
            if invokes_alert:
                # We arrived into a place where alert will pop up so no moving and no ajax
                sel.click(sub_loc(sub), wait_ajax=False)
            else:
                select_n_move(sub_loc(sub))
        else:
            return False
    return True


def is_active(root):
    """ Checks if a button is currently depressed

    Args:
        root: The root button's name as a string.
    Returns: ``True`` if the button is depressed, ``False`` if not.
    """
    el = sel.element(root_loc(root))
    class_att = sel.get_attribute(el, 'class').split(" ")
    if "over" in class_att:
        return True
    else:
        return False


def is_greyed(root, sub=None):
    """ Checks if a button is greyed out.

    Args:
        root: The root button's name as a string.
    Returns: ``True`` if the button is greyed, ``False`` if not.
    """
    if sub:
        btn = sub_loc(sub)
    else:
        btn = root_loc(root)

    el = sel.element(btn)
    class_att = sel.get_attribute(el, 'class').split(" ")

    if sub:
        if "tr_btn_disabled" in class_att:
            return True
    else:
        if "dis" in class_att:
            return True
    return False
