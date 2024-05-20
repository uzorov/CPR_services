public class MessageInfo
{
    public string Body { get; set; }
    public string BodyType { get; set; }
    public string Subject { get; set; }
    public List<EmployeeInfo> Rerecipients { get; set; }
}

public class EmployeeInfo
{
    public string Email { get; set; }
}
