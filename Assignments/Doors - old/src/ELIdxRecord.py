def ELIdxRecord(DfTR,params,section,duration,subtrial,event,reward,punishment):

    # Create empty dictionary.
    dict = {}

    # Index Increment.
    params["idxTR"] += 1

    # Move data in Dict into Df.
    dict["Index"] = params["idxTR"]
    dict["subjectID"] = params["subjectID"]
    dict["Session"] = params["Session"]
    dict["Version"] = params["Version"]
    dict["Section"] = section
    dict["Subtrial"] = subtrial
    dict["Event"] = event
    dict["Reward"] = str(reward)
    dict["Punishment"] = str(punishment)

    dict["Duration(ms)"] = duration * 1000

    DfTR = DfTR.append(dict, ignore_index=True)
    DfTR.to_csv(params['outFileTrackerLog'], mode='a', sep=',', encoding='utf-8', index=False, header=False)

    return DfTR

