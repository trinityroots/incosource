from odoo import api, models, fields
from .query_list_wiz import QueryList
from .func_list_wiz import do_update, do_query, do_concat, do_concat_loop
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class ChangeEffectiveWiz(models.TransientModel):
    _name = "change.effective.wizard"

    # Define wizard field
    effective_date = fields.Datetime(
        string="Effective Date",
        help="Date at which the transfer is processed")
    rewrite_related_picking = fields.Boolean(
        string="Apply to Other Stock Picking",
        default=False,
        help="Also Apply to Other Stock Picking Which Has the Same Source Document Name")

    # Reminder when selecting future date rather than today
    @api.onchange('effective_date')
    def _effective_future(self):
        for selected in self.env['stock.picking'].browse(
                self._context.get('active_ids', [])):
            selected.date_done = self.effective_date
            current_date = datetime.now()

            # Compare today's date with selected date
            if self.effective_date and self.effective_date > current_date:
                # print("Future date is selected by user")
                _logger.debug("Future date is selected by user")
                return {
                    'warning': {
                        'title': 'Reminder',
                        'message': 'The date selected is still in the future. If you sure with the choice, '
                                   'you can ignore this message and proceed with your date selection',
                    },
                }

    # Saving record
    def update_effective_date(self):
        query = QueryList()
        print('------------------------------------\n', query)
        for record in self.env['stock.picking'].browse(
                self._context.get('active_ids', [])):

            # Define fields that called to wizard (model.Transient) from
            # stock.picking model (model.Models)
            pulled_name = record.name
            pulled_origin_name = record.origin
            concat_pulled_name = do_concat(pulled_name)

            if pulled_name and pulled_origin_name is True:
                # print("Picking name & origin document successfully pulled")
                _logger.debug(
                    "Picking name & origin document successfully pulled")
            else:
                # print("Either Picking name or Origin Document is not found")
                _logger.debug(
                    "Either Picking name or Origin Document is not found")

            # Check internal or external transfer first
            # If pulled_origin_name is True, then it's external transfer
            if pulled_origin_name:

                # This is external transfer
                # Check if rewrite_related_picking checkbox is not set
                if not self.rewrite_related_picking:
                    if record.picking_type_id.code == 'outgoing' \
                            and record.sale_id:
                        record.sale_id.date_order = self.effective_date
                    elif record.picking_type_id.code == 'incoming' \
                            and record.purchase_id:
                        record.purchase_id.date_approve = self.effective_date
                    # If rewrite_related_picking is not checked (False) then update current picking only
                    # Update stock_picking
                    do_update(
                        query.update_stock_picking_by_name,
                        self.effective_date,
                        pulled_name)
                    _logger.debug("Successfully changed stock_picking")

                    # Update sale_order
                    do_update(
                        query.update_sale_order,
                        self.effective_date,
                        pulled_origin_name)
                    _logger.debug("Successfully changed sale_order")

                    # Update account_move
                    do_update(
                        query.update_journal_entry,
                        self.effective_date,
                        concat_pulled_name)
                    _logger.debug("Successfully changed account_move")

                    # Update account_move_line
                    do_update(
                        query.update_journal_entry_line,
                        self.effective_date,
                        concat_pulled_name)
                    _logger.debug("Successfully changed account_move_line")

                    # Update stock_move
                    do_update(
                        query.update_stock_move,
                        self.effective_date,
                        pulled_name)
                    _logger.debug("Successfully changed stock_move")

                    # Update stock_move_line
                    do_update(
                        query.update_stock_move_line,
                        self.effective_date,
                        pulled_name)
                    _logger.debug("Successfully changed stock_move_line")

                else:
                    # If rewrite_related_picking is checked (True) then update all related picking based on origin
                    # Find SO or PO based on origin name
                    do_query(
                        query.find_name_from_stock_picking,
                        pulled_origin_name)
                    pulled_stock_picking = [pulled_stock_picking_as_row[0]
                                            for pulled_stock_picking_as_row in self.env.cr.fetchall()]
                    percentage_stock_picking = do_concat_loop(
                        pulled_stock_picking)

                    pulled_stock_picking_tuples = tuple(pulled_stock_picking)
                    if pulled_stock_picking_tuples == ():
                        _logger.debug(
                            "Not changing anything because origin is not set")
                    else:
                        # Update stock_picking
                        do_update(
                            query.update_stock_picking_by_origin,
                            self.effective_date,
                            pulled_origin_name)
                        _logger.debug("Successfully changed stock_picking")

                        # Update sale_order
                        do_update(
                            query.update_sale_order,
                            self.effective_date,
                            pulled_origin_name)
                        _logger.debug("Successfully changed sale_order")

                        # Update journal entry
                        do_update(
                            query.update_journal_entry_by_ref_tuple,
                            self.effective_date,
                            percentage_stock_picking)
                        _logger.debug("Successfully changed account_move")

                        # Update journal items
                        do_update(
                            query.update_journal_entry_line_by_ref_tuple,
                            self.effective_date,
                            percentage_stock_picking)
                        _logger.debug("Successfully changed account_move_line")

                        # Update Stock Move
                        do_update(
                            query.update_stock_move_by_ref_tuple,
                            self.effective_date,
                            pulled_stock_picking_tuples)
                        _logger.debug("Successfully changed stock_move")

                        # Update stock move line
                        do_update(
                            query.update_stock_move_line_by_ref_tuple,
                            self.effective_date,
                            pulled_stock_picking_tuples)
                        _logger.debug("Successfully changed stock_move_line")

            else:
                # Update internal transfer
                do_update(
                    query.update_stock_picking_by_name,
                    self.effective_date,
                    pulled_name)
                _logger.debug("Successfully changed stock_picking")

                # Update stock move
                do_update(
                    query.update_stock_move,
                    self.effective_date,
                    pulled_name)
                _logger.debug("Successfully changed stock_move")

                # Update stock_move_line
                do_update(
                    query.update_stock_move_line,
                    self.effective_date,
                    pulled_name)
                _logger.debug("Successfully changed stock_move_line")
