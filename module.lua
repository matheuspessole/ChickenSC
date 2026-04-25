(function(a, b, c, d, e)
    local log_table = {
        "╔════════════════════════════════════════╗\n",
        "║           ChickenSC - DIAGNOSTIC       ║\n",
        "╚════════════════════════════════════════╝\n\n",
        "> System:          " .. a .. "\n",
        "> Processor:       ".. b .. "\n",
        "> Architecture:    " .. c.."\n",
        "> RAM:             " .. d .." GB\n",
        "> Storage:         " .. e .."GB \n\n",
        "───────────────────────────────────────────\n",
        "               END OF REPORT                  \n",
        "───────────────────────────────────────────\n"
    }
    return table.concat(log_table)
end)